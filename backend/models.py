from django.db import models

# Create your models here.
class Personaje(models.Model):
    x = models.IntegerField(default=50)
    y = models.IntegerField(default=50)