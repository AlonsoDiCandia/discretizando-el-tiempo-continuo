from django.shortcuts import render
from backend.models import Personaje
from django.http import HttpResponse

import json

# Create your views here.

def seleccion_personaje(request):
    personajes_db = Personaje.objects.all()
    
    personajes = []
    
    for p in personajes_db:
        foo = {
            "nombre": p.nombre,
            "imagen_url": p.imagen.url
        }
        
        personajes.append(foo)
    return render(request, "seleccion_personaje.html", {"personajes": personajes}, )