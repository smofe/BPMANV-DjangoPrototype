from celery import Celery

app = Celery()

@app.task
def test():
    print("Hello World")


@app.task
def test2():
    print("Every 5 seconds...")

