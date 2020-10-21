from celery import Celery
from celery import shared_task


# BROKER_URL = 'redis://localhost:6379/0'
app = Celery()


@app.task
def Tik():
    print('Tik!')


@app.task
def Tak():
    print('Tak!')
