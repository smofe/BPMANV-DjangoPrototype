from celery import Celery

app = Celery('hello')

@app.task
def testTask(patient_object):
    patient_object.age = 999
    patient_object.save()
    print("Woohooo")

