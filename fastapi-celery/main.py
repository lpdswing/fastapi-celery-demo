from fastapi import FastAPI, BackgroundTasks
from celery.result import AsyncResult
from worker.celery_app import celery_app
from worker.celery_worker import add

app = FastAPI()


def celery_on_message(body):
    print(body)

def background_on_message(task):
    print(task.get(on_message=celery_on_message, propagate=False))





@app.get('/get_res/{id}')
async def get_res(id):
    '''查询结果,这里写的比较简单'''
    task = AsyncResult(id=id, app=celery_app)
    # print(task.successful())
    if task.successful():
        return {'res':task.get()}


@app.get('/call_add')
async def call_add(background_task: BackgroundTasks):
    # task =  celery_app.send_task(
    #     'worker.celery_worker.add', args = [4,5]
    # )
    # print(task)
    # background_task.add_task(background_on_message, task)
    add.delay(3,4)
    return {"message": "add called"}


@app.get("/{word}")
async def root(word: str, background_task: BackgroundTasks):
    task = celery_app.send_task(
        "worker.celery_worker.test_celery", args=[word])
    print(task)
    background_task.add_task(background_on_message, task)
    return {"message": "Word received"}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app,port=8000)

    # celery worker -A worker.celery_worker -l info  -Q test-queue -P gevent