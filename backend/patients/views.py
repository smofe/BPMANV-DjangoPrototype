from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Patient, PatientState, Entity, Inventory, GameInstance
from .serializers import *
import datetime
from .utils import *
import json


class GameInstanceList(generics.ListCreateAPIView):
    """
    List all patients, or create a new patient.
    """
    queryset = GameInstance.objects.all()
    serializer_class = GameInstanceSerializer


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


@api_view(['PATCH'])
def all_patients_view(request):
    """
    Sets the paramaters in the JSON for all patients
    """
    if request.method == 'PATCH':
        return patch_all_patients(request.data)


@api_view(['PATCH'])
def all_patients_start(request):
    """
    Sets the start_time to datetime.now() for all patients
    """
    json = {"start_time": str(datetime.now())}
    if request.method == 'PATCH':
        return patch_all_patients(json)


def patch_all_patients(data):
    patients = Patient.objects.all()
    for patient in patients:
        serializer = PatientSerializer(patient, data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(data, status=status.HTTP_200_OK)


@api_view(['PATCH'])
def patient_change_state(request, pk):
    """
    Invoke a phase change on a patient
    """
    patient = get_object_or_404(Patient, pk=pk)

    if request.method == 'PATCH':
        return change_state_of_one_patient(patient)


def change_state_of_one_patient(patient):
    primary_condition = patient.patient_state.primary_condition
    primary_condition_is_met = PatientSerializer(patient, context={'fields': [primary_condition]}).data.get(
        primary_condition)

    secondary_condition = patient.patient_state.secondary_condition
    secondary_condition_is_met = PatientSerializer(patient, context={'fields': [secondary_condition]}).data.get(
        secondary_condition)

    try:
        next_state_A_id = patient.patient_state.next_state_A.id
        next_state_B_id = patient.patient_state.next_state_B.id
        next_state_C_id = patient.patient_state.next_state_C.id
    except AttributeError:
        print("No pointer on next state!")
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if primary_condition_is_met:
        new_patient_state_pk = next_state_C_id
    elif secondary_condition_is_met:
        new_patient_state_pk = next_state_B_id
    else:
        new_patient_state_pk = next_state_A_id

    next_state_json = {"patient_state": new_patient_state_pk}
    serializer = PatientSerializer(patient, data=next_state_json)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EntityDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Lists one entity in detail, update an entity or delete one.
    """
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer


class InventoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer


@api_view(['GET', 'PATCH'])
def game_instance_detail(request, pk):
    instance = get_object_or_404(GameInstance, pk=pk)

    if request.method == 'GET':
        instance_serializer = GameInstanceDetailSerializer(instance)
        return Response(instance_serializer.data)


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
        return Response(serializer.data)


@api_view(['PATCH'])
def inventory_exchange(request, sender_pk, receiver_pk):
    """
    Transfers specified materials from the senders inventory to the receivers inventory if possible
    """
    sender = get_object_or_404(Entity, pk=sender_pk)
    receiver = get_object_or_404(Entity, pk=receiver_pk)

    if request.method == 'PATCH':
        # save_json_to_log(request)
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
                return Response("The inventory requested from does not contain the specified quantities of material", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("No negative numbers are allowed in an exchange request", status=status.HTTP_400_BAD_REQUEST)