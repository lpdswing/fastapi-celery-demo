
from time import sleep

from celery import current_task, Task

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
                                  meta={'process_percent': i*10})
    return f"test task return {word}"


# 根据任务状态执行不同操作
@celery_app.task(base=MyTask)
def add(x,y):
    raise KeyError
    return x+y