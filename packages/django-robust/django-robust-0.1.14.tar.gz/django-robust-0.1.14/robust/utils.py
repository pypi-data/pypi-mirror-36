import json
import sys
import traceback
from datetime import datetime, timedelta

from django.conf import settings
from django.utils import timezone
from django.utils.inspect import getargspec
from django.utils.module_loading import import_string

from .exceptions import Retry as BaseRetry


def get_kwargs_processor_cls():
    processor_cls_path = getattr(settings, 'ROBUST_PAYLOAD_PROCESSOR', 'robust.utils.PayloadProcessor')
    return import_string(processor_cls_path)


def wrap_payload(payload):
    return get_kwargs_processor_cls().wrap_payload(payload)


def unwrap_payload(payload):
    return get_kwargs_processor_cls().unwrap_payload(payload)


class PayloadProcessor(object):
    @staticmethod
    def wrap_payload(payload):
        return payload

    @staticmethod
    def unwrap_payload(payload):
        return payload


class ArgsWrapper(object):
    def __init__(self, wrapper, eta=None, delay=None):
        """
        :type wrapper: TaskWrapper
        :type eta: datetime
        :type delay: timedelta
        """
        self.wrapper = wrapper

        if eta and delay:
            raise RuntimeError('both eta and delay provided')

        if delay:
            eta = timezone.now() + delay

        self.eta = eta

    def delay(self, *args, **kwargs):
        return self.wrapper.delay_with_task_kwargs({'eta': self.eta}, *args, **kwargs)


class TaskWrapper(object):
    bind = False
    fn = None
    retries = None
    tags = []
    Retry = BaseRetry

    def __new__(cls, *args, **kwargs):
        if cls.bind:
            return cls.fn(cls, *args, **kwargs)
        return cls.fn(*args, **kwargs)

    @classmethod
    def with_task_kwargs(cls, eta=None, delay=None):
        """
        :type eta: datetime
        :type delay: timedelta
        :rtype ArgsWrapper
        """
        return ArgsWrapper(cls, eta=eta, delay=delay)

    @classmethod
    def delay_with_task_kwargs(cls, _task_kwargs, *args, **kwargs):
        """
        :rtype robust.models.Task
        """

        name = '{}.{}'.format(cls.__module__, cls.__name__)

        if args:
            fn_args, _, _, _ = getargspec(cls.fn)
            if cls.bind:
                fn_args = fn_args[1:]

            if len(args) > len(fn_args):
                raise TypeError('wrong args number passed for {}'.format(name))

            positional = fn_args[:len(args)]
            for key in positional:
                if key in kwargs:
                    raise TypeError('{} used as positional argument for {}'.format(key, name))

            kwargs = dict(kwargs)
            for key, value in zip(fn_args, args):
                kwargs[key] = value

        wrapped_kwargs = wrap_payload(kwargs)

        if getattr(settings, 'ROBUST_ALWAYS_EAGER', False):
            json.dumps(wrapped_kwargs)  # checks kwargs is JSON serializable
            kwargs = unwrap_payload(wrapped_kwargs)
            if cls.bind:
                return cls.fn(cls, **kwargs)
            return cls.fn(**kwargs)

        from .models import Task
        _kwargs = {
            'tags': cls.tags,
            'retries': cls.retries
        }
        _kwargs.update(_task_kwargs)
        return Task.objects.create(name=name, payload=wrapped_kwargs, **_kwargs)

    @classmethod
    def delay(cls, *args, **kwargs):
        """
        :rtype robust.models.Task
        """
        return cls.delay_with_task_kwargs({}, *args, **kwargs)

    @classmethod
    def retry(cls, eta=None, delay=None):
        """
        :type eta: datetime
        :type delay: timedelta
        """
        etype, value, tb = sys.exc_info()
        trace = None
        if etype:
            trace = ''.join(traceback.format_exception(etype, value, tb))
        try:
            raise cls.Retry(eta=eta, delay=delay, trace=trace)
        finally:
            del tb


def task(bind=False, tags=None, retries=None):
    def decorator(fn):
        retry_cls = type('{}{}'.format(fn.__name__, 'Retry'), (BaseRetry,), {})
        retry_cls.__module__ = fn.__module__

        task_cls = type(fn.__name__, (TaskWrapper,), {
            'fn': staticmethod(fn),
            'retries': retries,
            'tags': tags,
            'bind': bind,
            'Retry': retry_cls
        })
        task_cls.__module__ = fn.__module__

        return task_cls

    return decorator


@task()
def cleanup():
    from .models import Task
    now = timezone.now()
    succeed_task_expire = now - getattr(settings, 'ROBUST_SUCCEED_TASK_EXPIRE', timedelta(hours=1))
    troubled_task_expire = now - getattr(settings, 'ROBUST_FAILED_TASK_EXPIRE', timedelta(weeks=1))

    Task.objects \
        .filter(events__status__in={Task.FAILED, Task.RETRY},
                status__in={Task.FAILED, Task.SUCCEED},
                updated_at__lte=troubled_task_expire) \
        .delete()

    Task.objects \
        .exclude(events__status__in={Task.FAILED, Task.RETRY}) \
        .filter(status=Task.SUCCEED, updated_at__lte=succeed_task_expire) \
        .delete()
