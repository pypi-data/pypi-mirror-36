# -*- coding: utf-8 -*-

import uuid
import importlib
import logging
import time
import functools

from threading import local

try:
    from celery import (
        Celery,
        signals,
    )
except ImportError:
    raise ImportError('To use queue module, you must install celery.')
try:
    from sqlalchemy import event
except:
    event = None

logger = logging.getLogger(__name__)
async_ctx = local()


class AsyncTask(object):
    __slots__ = (
        'task_id', 'module_name', 'func_name', 'args', 'kwargs',
        'countdown', 'send_after_commit', 'extra_celery_kwargs', 'apply_queue',
    )

    def __init__(
            self, module_name, func_name, args=None, kwargs=None,
            countdown=0, send_after_commit=False,
            apply_queue='queue', extra_celery_kwargs=None,
    ):
        mod = importlib.import_module(module_name)
        if not hasattr(mod, func_name):
            raise ValueError('Invalid API Endpoint is provided.')
        self.task_id = uuid.uuid1().hex
        self.module_name = module_name
        self.func_name = func_name
        self.args = args if args is not None else ()
        self.kwargs = kwargs if kwargs is not None else {}
        self.countdown = countdown if countdown >= 0 else 0
        self.send_after_commit = bool(send_after_commit)
        self.extra_celery_kwargs = extra_celery_kwargs if extra_celery_kwargs is not None else {}
        self.apply_queue = apply_queue

    def register(self):
        if self.send_after_commit:
            if hasattr(async_ctx, 'reged_tasks'):
                async_ctx.reged_tasks.add(self)
            else:
                async_ctx.reged_tasks = {self}
        else:
            raise ValueError('Cannot register task without send_after_commit flag.')

    def send(self, async_api):
        return async_api.si(
            self.module_name, self.func_name,
            *self.args,
            **self.kwargs
        ).apply_async(
            countdown=self.countdown,
            queue=self.apply_queue,
            **self.extra_celery_kwargs
        )


def make_send_task(async_api, apply_queue):
    return functools.partial(send_task, async_api=async_api, apply_queue=apply_queue)


def send_task(module_name, api_name, *args, countdown=0, async_api=None, apply_queue=None, send_after_commit=False, extra_celery_kwargs=None, **kwargs):
    if not async_api or not apply_queue:
        raise RuntimeError('create send_task using make_send_task.')
    task = AsyncTask(
        module_name=module_name,
        func_name=api_name,
        args=args,
        kwargs=kwargs,
        countdown=countdown,
        send_after_commit=send_after_commit,
        extra_celery_kwargs=extra_celery_kwargs,
        apply_queue=apply_queue,
    )
    if send_after_commit:
        task.register()
    else:
        task.send(async_api)
    return task.task_id


def make_async_task(function_executor, retry_wait=5):
    def _f(self, module_name, api_name, *args, **kwargs):
        if 'retry_wait' in kwargs:
            retry_wait_ = kwargs['retry_wait']
            del kwargs['retry_wait']
        else:
            retry_wait_ = retry_wait

        return async_task(self, module_name, api_name, retry_wait_, function_executor, *args, **kwargs)
    return _f


def async_task(self, module_name, api_name, retry_wait=5, func_executor=None, *args, **kwargs):
    try:
        mod = importlib.import_module(module_name)
        func = getattr(mod, api_name)
        return func_executor(func)(*args, **kwargs)
    except Exception as e:
        self.retry(exc=e, countdown=retry_wait)


def register_to_celery(celery_broker, celery_config, async_task, max_retries=12, DBSession=None):
    def send_after_commit_tasks(session):
        if not hasattr(async_ctx, 'reged_tasks'):
            return
        for task in async_ctx.reged_tasks:
            task.send(async_api)
        delattr(async_ctx, 'reged_tasks')

    broker = 'amqp://{user}:{password}@{host}:{port}/{vhost}'.\
        format(**celery_broker)

    app = Celery(broker=broker)
    app.conf.update(**celery_config)

    async_api = app.task(max_retries=max_retries, bind=True)(async_task)
    if DBSession:
        if event:
            event.listens_for(DBSession, 'after_commit')(send_after_commit_tasks)
        else:
            raise ImportError('You must install sqlalchemy first.')

    return app, async_api


def init_celery_log(loglevel=logging.INFO, **kwargs):
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s [%(process)d] [%(levelname)s] %(name)s: %(message)s')
    handler.setFormatter(formatter)
    log = logging.getLogger('')
    log.addHandler(handler)
    log.setLevel(loglevel)
    return log
