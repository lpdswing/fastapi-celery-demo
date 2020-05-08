# FastApi-Celery

## 启动fastapi服务

> uvicorn main:app

## 启动worker

> celery worker -A worker.celery_worker -l info -f celery.log -Q test-queue -P gevent

- win10 不加-P gevent会报错,也可以-P eventlet,我这里用eventlet报错了,后来发现是localhost的锅



- 异常情况

    - backend = 'redis://:123456@127.0.0.1:6379/0' 这里127.0.0.1用localhost替代的话
    会出现
    `[2020-05-07 18:26:07,064: ERROR/MainProcess] consumer: Cannot connect to redis://:**@localhost:6379/1: Error 11001 connecting to localhost:6379. No address found..
    Trying again in 16.00 seconds... (8/100)`
    这种错误 ... 
    让我在风中凌乱一会

## 定时任务

- 发送定时任务
   
  > celery beat -A worker.celery_worker -l info

- 启动定时任务worker

    > celery worker -A worker.celery_worker -l info -P eventlet
