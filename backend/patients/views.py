from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Patient, PatientState
from .serializers import PatientSerializer, PatientListSerializer, PatientStateSerializer
import datetime


@csrf_exempt
@api_view(['GET', 'POST'])
def patient_list(request):
    """
    List all patients, or create a new patient.
    """
    if request.method == 'GET':
        patients = Patient.objects.all()
        serializer = PatientListSerializer(patients, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'POST'])
def patient_state_list(request):
    """
    List all patient states, or create a new patient state.
    """
    if request.method == 'GET':
        patient_states = PatientState.objects.all()
        serializer = PatientStateSerializer(patient_states, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PatientStateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def patient_detail(request, pk):
    """
    Lists one patient in detail, update a patient or delete one.
    """
    try:
        patient = Patient.objects.get(pk=pk)
    except Patient.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PatientSerializer(patient)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PatientSerializer(patient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        patient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def patient_state_detail(request, pk):
    """
        Lists one patient state in detail, update a patient state or delete one.
    """
    try:
        patient_state = PatientState.objects.get(pk=pk)
    except PatientState.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PatientStateSerializer(patient_state)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PatientStateSerializer(patient_state, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        patient_state.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def patient_check_field(request, pk, field):
    """
    Retrieve one specific field of a patient
    """
    try:
        patient = Patient.objects.get(pk=pk)
    except Patient.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PatientSerializer(patient, context={'fields': [field]})
        current_date_and_time = datetime.datetime.now()
        current_date_and_time += datetime.timedelta(seconds = 120)
        current_time = current_date_and_time.strftime("%H:%M:%S")
        return Response({'finishing_time': current_time, field: serializer.data})

@csrf_exempt
@api_view(['PUT'])
def patient_change_state(request,pk):
    """
    Invoke a phase change on a patient
    """
    try:
        patient = Patient.objects.get(pk=pk)
    except Patient.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        primary_condition = PatientSerializer(patient, context={'fields': ['patient_state']}).data.get('patient_state').get('primary_condition')
        primary_condition_boolean = PatientSerializer(patient, context={'fields': [primary_condition]}).data.get(primary_condition)

        secondary_condition = PatientSerializer(patient, context={'fields': ['patient_state']}).data.get(
            'patient_state').get('secondary_condition')
        secondary_condition_boolean = PatientSerializer(patient, context={'fields': [secondary_condition]}).data.get(
            secondary_condition)

        if primary_condition_boolean:
            next_state_variant = 'C'
        elif secondary_condition_boolean:
            next_state_variant = 'B'
        else:
            next_state_variant = 'A'

        next_state_id = PatientSerializer(patient, context={'fields': ['patient_state']}).data.get('patient_state').get("next_state_" + next_state_variant + "_id")
        next_state_json = {"current_state_id": next_state_id}
        serializer = PatientSerializer(patient, data=next_state_json)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

