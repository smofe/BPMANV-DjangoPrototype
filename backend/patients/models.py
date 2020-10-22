from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from datetime import datetime

default_datetime = datetime(2000, 1, 1)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class PatientState(models.Model):
    respiration_rate = models.IntegerField(default=20)
    heart_rate = models.IntegerField(default=70)
    oxygen_saturation = models.IntegerField(default=95)
    blood_pressure_sys = models.IntegerField(default=120)
    # ist gehfähig
    is_ambulant = models.BooleanField(default=True)
    # hat spritzende Blutung
    has_sputtering_bleeding = models.BooleanField(default=False)
    # blutet
    is_bleeding = models.BooleanField(default=False)
    # ist regungslos
    is_motionless = models.BooleanField(default=False)
    # hat Zyanose
    has_cyanosis = models.BooleanField(default=False)

    next_state_A = models.ForeignKey(to='PatientState', null=True, blank=True, on_delete=models.CASCADE, related_name="A")
    next_state_B = models.ForeignKey(to='PatientState', null=True,blank=True, on_delete=models.CASCADE, related_name="B")
    next_state_C = models.ForeignKey(to='PatientState', null=True,blank=True, on_delete=models.CASCADE, related_name="C")
    duration = models.IntegerField(default=5)
    description = models.TextField(default='This is a patient.')
    primary_condition = models.CharField(max_length=50, default="is_ventilated")
    secondary_condition = models.CharField(max_length=50, default="has_tourniquet")


class GameInstance(models.Model):
    max_players = models.IntegerField(default=50)
    start_time = models.DateTimeField(default=default_datetime)


class Patient(models.Model):
    game_instance = models.ForeignKey(GameInstance, models.CASCADE, default=1)
    name = models.CharField(max_length=50, default='unknown')
    age = models.IntegerField(default=9999)
    gender = models.CharField(max_length=20, default='none')
    hair_color = models.CharField(max_length=20, default='Orange')
    patient_state = models.ForeignKey(PatientState, default=1, on_delete=models.CASCADE)
    next_phase_timestamp = models.DateTimeField(default=datetime.now())

    is_in_recovery_position = models.BooleanField(default=False)
    is_ventilated = models.BooleanField(default=False)
    has_tourniquet = models.BooleanField(default=False)
    get_infusion = models.BooleanField(default=False)


class Entity(models.Model):
    name = models.CharField(max_length=50, default='Player')


class Inventory(models.Model):
    entity = models.OneToOneField(Entity, on_delete=models.CASCADE)
    max_item_amount = models.IntegerField(default=200)
    current_item_amount = models.IntegerField(default=0)
    material_druckverband = models.IntegerField(default=0)
    material_guedeltubus = models.IntegerField(default=0)
    material_rettungsdecke = models.IntegerField(default=0)
    material_blutdruckmessgeraet = models.IntegerField(default=0)
    material_infusion = models.IntegerField(default=0)
    material_pflaster = models.IntegerField(default=0)
    material_schmerzmittel = models.IntegerField(default=0)
    material_tourniquet = models.IntegerField(default=0)
    material_beatmungsgeraet = models.IntegerField(default=0)
    material_defibrilator = models.IntegerField(default=0)
    material_sauerstoffflasche = models.IntegerField(default=0)


class Vehicle(models.Model):
    car_type = models.CharField(max_length=50, default='RTW')
    funk_name = models.CharField(max_length=50, default='unknown')
    arrival_time = models.DurationField(default=5)
    distance = models.IntegerField(default=2)
    manpower = models.IntegerField(default=2)


class RescueForce(models.Model):
    qualification = models.CharField(max_length=50, default='Rettungshelfer')
    actual_role = models.CharField(max_length=50, default='Einsatzleiter')
    dedicated_car = models.CharField(max_length=50, default='unknown')

