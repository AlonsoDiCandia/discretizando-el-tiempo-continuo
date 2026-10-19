from django.shortcuts import render
from backend.models import Personaje, PersonajeSeleccionado
from django.http import HttpResponse

import json

# Create your views here.

def seleccion_personaje(request):
    personajes_db = Personaje.objects.all()
    
    personajes = []
    
    for p in personajes_db:
        foo = {
            "id": p.id,
            "nombre": p.nombre,
            "imagen_url": p.imagen.url
        }
        
        personajes.append(foo)
        
    ps = PersonajeSeleccionado.objects.first()
    
    return render(request, "seleccion_personaje.html", {"personajes": personajes, "personaje_seleccionado": {"nombre": ps.seleccionado.nombre, "imagen_url": ps.seleccionado.imagen.url}}, )