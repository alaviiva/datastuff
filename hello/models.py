from django.db import models

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)

class Sensordata(models.Model):
    date = models.DateTimeField()
    sensor1 = models.FloatField()
    sensor2 = models.FloatField()
    sensor3 = models.FloatField()
    sensor4 = models.FloatField()

