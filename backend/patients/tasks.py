from datetime import datetime
from celery import Celery

from . import views
from .models import Patient
from .serializers import PatientSerializer

app = Celery()

@app.task
def test():
    print("Hello World")



@app.task
def test2():
    print("Every 5 seconds...")

@app.task
def change_phase():
    all_patients = Patient.objects.all()
    print(all_patients)
    for patient in all_patients:
        print("Patient", patient)
        actual_time = datetime.now()
        print("patientstate durch serializer zugreifen:", patient.patient_state)
        #duration = patient.patient_state.duration

        #print("patientstate durch serializer zugreifen:", duration)
'''
        start_of_phase = patient.start_time
        end_of_phase = start_of_phase + datetime.timedelta(seconds=duration)
        if actual_time > end_of_phase:
            data = views.patient_change_state(patient)
            print(data)'''
