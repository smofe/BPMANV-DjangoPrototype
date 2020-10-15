from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Patient, PatientState
from .serializers import PatientSerializer, PatientStateSerializer
import datetime


class PatientList(generics.ListCreateAPIView):
    """
    List all patients, or create a new patient.
    """
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class PatientStateList(generics.ListCreateAPIView):
    """
    List all patient states, or create a new patient state.
    """
    queryset = PatientState.objects.all()
    serializer_class = PatientStateSerializer


class PatientDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Lists one patient in detail, update a patient or delete one.
    """
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class PatientStateDetail(generics.RetrieveUpdateDestroyAPIView):
    """
        Lists one patient state in detail, update a patient state or delete one.
    """
    queryset = PatientState.objects.all()
    serializer_class = PatientStateSerializer



@api_view(['GET'])
def patient_check_field(request, pk, field):
    """
    Retrieve one specific field of a patient
    """
    patient = get_object_or_404(Patient, pk=pk)

    if request.method == 'GET':
        serializer = PatientSerializer(patient, context={'fields': [field]})
        current_date_and_time = datetime.datetime.now()
        current_date_and_time += datetime.timedelta(seconds = 120)
        current_time = current_date_and_time.strftime("%H:%M:%S")
        return Response({'finishing_time': current_time, field: serializer.data})


@api_view(['PUT'])
def patient_change_state(request,pk):
    """
    Invoke a phase change on a patient
    """
    patient = get_object_or_404(Patient, pk=pk)

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

