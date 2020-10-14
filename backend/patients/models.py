from django.db import models
from .tasks import testTask
from datetime import datetime, timedelta


class Patient(models.Model):
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=20, default='none')
    hair_color = models.CharField(max_length=20, default='Orange')
    current_state_id = models.IntegerField(default=0)
    is_cured = models.BooleanField(default=False)

    def changeState(self):

        testTask.apply_async(args=[self], eta=datetime.now() + timedelta(seconds=10))



class PatientState(models.Model):
    respiration_rate = models.IntegerField(default=20)
    heart_rate = models.IntegerField(default=70)
    next_state_id = models.IntegerField(default=0)
    description = models.TextField(default = '')
