from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Patient, PatientState, Entity, Inventory
from .serializers import PatientSerializer, PatientStateSerializer, EntitySerializer, InventorySerializer
from datetime import datetime
from .utils import *


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
        current_date_and_time += datetime.timedelta(seconds=120)
        current_time = current_date_and_time.strftime("%H:%M:%S")
        return Response({'finishing_time': current_time, field: serializer.data})


@api_view(['PUT'])
def patient_change_state_request(request, pk):
    """
    Invoke a phase change on a patient
    """
    patient = get_object_or_404(Patient, pk=pk)

    if request.method == 'PUT':
        primary_condition = PatientSerializer(patient, context={'fields': ['patient_state']}).data.get(
            'patient_state').get('primary_condition')
        primary_condition_boolean = PatientSerializer(patient, context={'fields': [primary_condition]}).data.get(
            primary_condition)

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

        next_id = PatientSerializer(patient, context={'fields': ['patient_state']}).data.get('patient_state').get(
            "next_state_" + next_state_variant + "_id")
        next_state_json = {"current_state_id": next_id}
        serializer = PatientSerializer(patient, data=next_state_json)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def change_state(request):
    all_patients = Patient.objects.all()
    for patient in all_patients:
        actual_time = datetime.now()
        duration = patient.patient_state.duration
       # print("patientstate durch serializer zugreifen:", patient.patient_state)
        serializer = PatientSerializer(patient)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def patient_change_state(patient):
    primary_condition = PatientSerializer(patient, context={'fields': ['patient_state']}).data.get('patient_state').get(
        'primary_condition')
    primary_condition_boolean = PatientSerializer(patient, context={'fields': [primary_condition]}).data.get(
        primary_condition)

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

    next_id = PatientSerializer(patient, context={'fields': ['patient_state']}).data.get('patient_state').get(
        "next_state_" + next_state_variant + "_id")
    next_state_json = {"current_state_id": next_id}
    serializer = PatientSerializer(patient, data=next_state_json)
    if serializer.is_valid():
        serializer.save()
    return serializer.data


class EntityDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Lists one entity in detail, update an entity or delete one.
    """
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer


class InventoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer


@api_view(['GET'])
def entity_inventory_details(request, pk):
    entity = get_object_or_404(Entity, pk=pk)

    if request.method == 'GET':
        serializer = InventorySerializer(entity.inventory)
        return Response(serializer.data)


@api_view(['GET'])
def patient_check_state(request, pk):
    patient = get_object_or_404(Patient, pk=pk)

    if request.method == 'GET':
        serializer = PatientStateSerializer(patient.patient_state)
        print("Blub")
        return Response(serializer.data)


@api_view(['PATCH'])
def inventory_exchange(request, sender_pk, receiver_pk):
    """
    Transfers specified materials from the senders inventory to the receivers inventory if possible
    """
    sender = get_object_or_404(Entity, pk=sender_pk)
    receiver = get_object_or_404(Entity, pk=receiver_pk)

    if request.method == 'PATCH':
        sender_json = InventorySerializer(sender.inventory).data
        receiver_json = InventorySerializer(receiver.inventory).data
        request_json = request.data
        if json_are_all_values_positive(request_json):
            if json_is_subset_of(request_json, sender_json):
                json_subtract_subset(sender_json, request_json)
                json_add_subset(receiver_json, request_json)
                sender_serializer = InventorySerializer(sender.inventory, data=sender_json)
                receiver_serializer = InventorySerializer(receiver.inventory, data=receiver_json)
                if sender_serializer.is_valid() and receiver_serializer.is_valid():
                    sender_serializer.save()
                    receiver_serializer.save()
                    return Response(receiver_serializer.data)
            else:
                return Response("The inventory requested from does not contain the specified quantities of material",
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("No negative numbers are allowed in an exchange request",
                            status=status.HTTP_400_BAD_REQUEST)
