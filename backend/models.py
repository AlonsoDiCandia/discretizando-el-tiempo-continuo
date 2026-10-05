from django.db import models

# Create your models here.
class Personaje(models.Model):
    x = models.IntegerField(default=50)
    y = models.IntegerField(default=50)
    velocidad = models.IntegerField(default=25)
    imagen = models.ImageField(upload_to='statics') # EN prod no hacer esto, usar un bucket