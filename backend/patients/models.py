from django.db import models


class Patient(models.Model):
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=20, default='none')
    hair_color = models.CharField(max_length=20, default='Orange')
    current_state_id = models.IntegerField(default=0)
    is_ventilated = models.BooleanField(default=False)
    has_tourniquet = models.BooleanField(default=False)


class PatientState(models.Model):
    respiration_rate = models.IntegerField(default=20)
    heart_rate = models.IntegerField(default=70)
    next_state_A_id = models.IntegerField(default=0)
    next_state_B_id = models.IntegerField(default=0)
    next_state_C_id = models.IntegerField(default=0)
    description = models.TextField(default='')
    primary_condition = models.CharField(max_length=50, default="is_ventilated")
    secondary_condition = models.CharField(max_length=50, default="has_tourniquet")
