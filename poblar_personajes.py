import os
import django

# 1. Configura la variable de entorno apuntando al settings de tu proyecto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'juego.settings')

# 2. Inicializa Django
django.setup()

from backend.models import Personaje

p1 = Personaje.objects.get_or_create(
    nombre = "pepe",
    x = 50,
    y = 50,
    velocidad = 25
)

p2 = Personaje.objects.get_or_create(
    nombre = "samael",
    x = 50,
    y = 50,
    velocidad = 25
)

p3 = Personaje.objects.get_or_create(
    nombre = "Don M",
    x = 50,
    y = 50,
    velocidad = 25
)
