from rest_framework import serializers
from .models import Patient, PatientState, Entity, Inventory


class GameInstanceSerializer(serializers.ModelSerializer):

    def get_field_names(self, *args, **kwargs):
        field_names = self.context.get('fields', None)
        if field_names:
            return field_names
        return super(GameInstanceSerializer, self).get_field_names(*args, **kwargs)

    class Meta:
        model = Patient
        fields = "__all__"


class GameInstanceDetailSerializer(serializers.ModelSerializer):
    patients = serializers.SerializerMethodField(method_name="get_patients")

    def get_field_names(self, *args, **kwargs):
        field_names = self.context.get('fields', None)
        if field_names:
            return field_names
        return super(GameInstanceDetailSerializer, self).get_field_names(*args, **kwargs)

    def get_patients(self, obj):
        patients = Patient.objects.all().filter(game_instance=obj)
        serializer = PatientListSerializer(patients, many=True)
        return serializer.data

    class Meta:
        model = Patient
        fields = "__all__"


class PatientSerializer(serializers.ModelSerializer):

    def get_field_names(self, *args, **kwargs):
        field_names = self.context.get('fields', None)
        if field_names:
            return field_names
        return super(PatientSerializer, self).get_field_names(*args, **kwargs)

    class Meta:
        model = Patient
        fields = "__all__"


class PatientListSerializer(serializers.ModelSerializer):
    def get_field_names(self, *args, **kwargs):
        field_names = self.context.get('fields', None)
        if field_names:
            return field_names
        return super(PatientListSerializer, self).get_field_names(*args, **kwargs)

    class Meta:
        model = Patient
        fields = ['id', 'name']


class PatientStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientState
        fields = "__all__"


class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = "__all__"


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = "__all__"