from celery import Celery
from .models import Patient, PatientState
from .serializers import PatientSerializer
import datetime

app = Celery()


@app.task
def test():
    print("Hello World")


@app.task
def test2():
    print("Every 5 seconds...")

@app.task
def check_patient_states():
    print("Checking state of all patients...")
    patients = Patient.objects.all()
    for patient in patients:
        next_phase_timestamp = PatientSerializer(patient, context={'fields': ['next_phase_timestamp']}).data
        print(next_phase_timestamp)
        #print(datetime.now())
    print(patients)

