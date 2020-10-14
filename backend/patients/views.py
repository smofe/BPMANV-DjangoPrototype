from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Patient, PatientState
from .serializers import PatientSerializer, PatientListSerializer, PatientStateSerializer
import time, datetime


@csrf_exempt
def patient_list(request):
    if request.method == 'GET':
        patients = Patient.objects.all()
        serializer = PatientListSerializer(patients, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PatientSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def patient_state_list(request):
    if request.method == 'GET':
        patient_states = PatientState.objects.all()
        serializer = PatientStateSerializer(patient_states, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PatientStateSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def patient_detail(request, pk):
    try:
        patient = Patient.objects.get(pk=pk)
    except Patient.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = PatientSerializer(patient)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = PatientSerializer(patient, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        patient.delete()
        return HttpResponse(status=204)

@csrf_exempt
def patientstate_detail(request, pk):
    try:
        patient_state = PatientState.objects.get(pk=pk)
    except PatientState.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = PatientStateSerializer(patient_state)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = PatientStateSerializer(patient_state, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        patient_state.delete()
        return HttpResponse(status=204)


def patient_check_field(request, pk, field):
    try:
        patient = Patient.objects.get(pk=pk)
    except Patient.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = PatientSerializer(patient, context={'fields': [field]})
        current_date_and_time = datetime.datetime.now()
        seconds_added = datetime.timedelta(seconds = 120)
        current_date_and_time += seconds_added
        current_time = current_date_and_time.strftime("%H:%M:%S")
        return JsonResponse({'finishing_time': current_time, field: serializer.data})

@csrf_exempt
def patient_change_state(request,pk):
    try:
        patient = Patient.objects.get(pk=pk)
    except Patient.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'PUT':
        next_state_id = PatientSerializer(patient, context={'fields': ['patient_state']}).data.get('patient_state').get('next_state_id')
        next_state_json = {"current_state_id": next_state_id}
        serializer = PatientSerializer(patient, data=next_state_json)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def test(request,pk):
    try:
        patient = Patient.objects.get(pk=pk)
    except Patient.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        patient.changeState()