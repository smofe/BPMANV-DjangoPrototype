from datetime import datetime, timedelta
from celery import Celery
from django.utils import timezone

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
    for patient in all_patients:
        actual_time = timezone.now()
        print(actual_time)
        if actual_time > patient.next_phase_timestamp:
            end_of_current_phase = patient.next_phase_timestamp
            views.change_state_of_one_patient(patient)
            duration = patient.patient_state.duration
            next_timestamp_json = {"next_phase_timestamp": end_of_current_phase + timedelta(seconds=duration)}
            serializer = PatientSerializer(patient, data=next_timestamp_json)
            if serializer.is_valid():
                serializer.save()
