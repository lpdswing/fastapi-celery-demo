from time import sleep

from celery import current_task, Task
from celery.utils.log import get_task_logger

from .celery_app import celery_app


class MyTask(Task):
    def on_success(self, retval, task_id, args, kwargs):
        print(f'task done: {retval}')
        return super(MyTask, self).on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print(f'task fail, reason:{exc}')
        return super(MyTask, self).on_failure(exc, task_id, args, kwargs, einfo)


@celery_app.task(acks_late=True)
def test_celery(word: str) -> str:
    for i in range(1, 11):
        sleep(1)
        current_task.update_state(state='PROGRESS',
                                  meta={'process_percent': i * 10})
    return f"test task return {word}"


# 根据任务状态执行不同操作
@celery_app.task(base=MyTask)
def add(x, y):
    raise KeyError
    return x + y

logger = get_task_logger(__name__)

# 绑定任务为实例
@celery_app.task(bind=True)
def add1(self, x, y):
    logger.info(self.request.__dict__)
    return x + y


# 定时/周期任务
@celery_app.task(bind=True)
def beat_task(self):
    return (f'beat task done: {self.request.id}')