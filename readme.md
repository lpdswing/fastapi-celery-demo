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

## 链式任务

- 启动 worker

 > celery worker -A worker.celery_worker -l info -P eventlet

- 请求接口

 > `http://127.0.0.1:8000/run_chain_task`

- 结果

```shell script
[2020-05-08 15:44:25,050: INFO/MainProcess] Received task: worker.celery_worker.arg1[b114400a-3077-460d-a29c-206911456532]
[2020-05-08 15:44:25,066: INFO/MainProcess] Received task: worker.celery_worker.arg2[e7a1bd1c-9716-4934-ac8a-273bd72f4f56]
[2020-05-08 15:44:25,075: INFO/MainProcess] Task worker.celery_worker.arg1[b114400a-3077-460d-a29c-206911456532] succeeded in 0.031000000002677552s: 3
[2020-05-08 15:44:25,078: INFO/MainProcess] Received task: worker.celery_worker.chain_task[76f7f14f-21e2-4b10-8d18-cacf4e1bf382]
[2020-05-08 15:44:25,079: INFO/MainProcess] Task worker.celery_worker.arg2[e7a1bd1c-9716-4934-ac8a-273bd72f4f56] succeeded in 0.0s: 6
[2020-05-08 15:44:25,081: INFO/MainProcess] Task worker.celery_worker.chain_task[76f7f14f-21e2-4b10-8d18-cacf4e1bf382] succeeded in 0.0s: 7

```

