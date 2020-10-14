from rest_framework import serializers
from .models import Patient, PatientState


class PatientSerializer(serializers.ModelSerializer):
    patient_state = serializers.SerializerMethodField(method_name="get_patient_state")

    def get_field_names(self, *args, **kwargs):
        field_names = self.context.get('fields', None)
        if field_names:
            return field_names
        return super(PatientSerializer, self).get_field_names(*args, **kwargs)

    def get_patient_state(self, obj):
        patient_state = PatientState.objects.get(pk=obj.current_state_id)
        serializer = PatientStateSerializer(patient_state, many=False)
        return serializer.data

    class Meta:
        model = Patient
        fields = ('age', 'gender', 'hair_color', 'current_state_id', 'patient_state', 'is_cured')

class PatientListSerializer(serializers.ModelSerializer):
    def get_field_names(self, *args, **kwargs):
        field_names = self.context.get('fields', None)
        if field_names:
            return field_names
        return super(PatientListSerializer, self).get_field_names(*args, **kwargs)

    class Meta:
        model = Patient
        fields = ['id']

class PatientStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientState
        fields = "__all__"
