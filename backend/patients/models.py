from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from datetime import datetime, timedelta


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

    next_state_A_id = models.IntegerField(default=0)
    next_state_B_id = models.IntegerField(default=0)
    next_state_C_id = models.IntegerField(default=0)
    description = models.TextField(default='This is a patient.')
    primary_condition = models.CharField(max_length=50, default="is_ventilated")
    secondary_condition = models.CharField(max_length=50, default="has_tourniquet")


class Patient(models.Model):
    name = models.CharField(max_length=50, default='unknown')
    age = models.IntegerField(default=9999)
    gender = models.CharField(max_length=20, default='none')
    hair_color = models.CharField(max_length=20, default='Orange')
    patient_state = models.ForeignKey(PatientState, default=1, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=datetime.now())
    delay_in_minutes = models.IntegerField(default=15)

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
    material_mullbinde = models.IntegerField(default=0)
    material_pflaster = models.IntegerField(default=0)
    material_schmerzmittel = models.IntegerField(default=0)
    material_verband = models.IntegerField(default=0)
    material_tourniquet = models.IntegerField(default=0)
    material_beatmungsgeraet = models.IntegerField(default=0)
    material_defibrilator = models.IntegerField(default=0)
    material_sauerstoffflasche = models.IntegerField(default=0)





