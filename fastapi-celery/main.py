import sys

from fastapi import FastAPI, BackgroundTasks
from celery.result import AsyncResult
from worker.celery_app import celery_app
from worker.celery_worker import run_chain_task

app = FastAPI()


def celery_on_message(body):
    if body.get('status') == 'PROGRESS':
        res = body.get('result')
        sys.stdout.write(f"\r任务进度: {res.get('process_percent')}%")
        sys.stdout.flush()
    else:
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
    task =  celery_app.send_task(
        'worker.celery_worker.add', args = [4,5]
    )
    print(task)
    background_task.add_task(background_on_message, task)
    return {"message": "add called"}

@app.get('/call_add1')
async def call_add1(background_task: BackgroundTasks):
    task =  celery_app.send_task(
        'worker.celery_worker.add1', args = [4,5]
    )
    print(task)
    background_task.add_task(background_on_message, task)
    return {"message": "add1 called"}

@app.get('/run_chain_task')
async def chain_task(background_task: BackgroundTasks):
    run_chain_task()
    return {"message": "run_chain_task called"}


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

