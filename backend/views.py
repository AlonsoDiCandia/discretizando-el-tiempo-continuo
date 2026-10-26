from django.shortcuts import render
from backend.models import Personaje, PersonajeSeleccionado
from django.http import HttpResponse
from backend.generar_imagen.Jugador import Jugador

import os
import numpy as np
import json
import cv2 

W = 1000
H = 500
PATH = os.getcwd()
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

def generar_imagen(request):
    p = PersonajeSeleccionado.objects.first().seleccionado
    jugador = Jugador(p)

    personaje = cv2.imread(PATH + p.imagen.url)
    personaje = cv2.resize(personaje, (100,100))

    # Inicio personaje
    x,y = p.x, p.y

    tesoro = cv2.imread("tesoro.jpg")
    tesoro = cv2.resize(tesoro, (100,100))

    # Inicio tesoro
    tx, ty = 600, 250

    img = np.full((H, W, 3), 255, dtype=np.uint8)
    # Personaje a la imagen
    cv2.line(img, (300,227), (300, 400), (100,200,100), 5)
    img[y:y+personaje.shape[0], x:x+personaje.shape[1]] = personaje
    
    img[ty:ty+tesoro.shape[0], tx:tx+tesoro.shape[1]] = tesoro


    # if jugador.hay_colision(x,y, personaje.shape[0], personaje.shape[1], tx,ty, tesoro.shape[0], tesoro.shape[1]):
    #     print("Colision con tesoro")
        
    # if jugador.hay_colision(x,y, personaje.shape[0], personaje.shape[1], 300, 227, 5, 200):
    #     print("Colision con la linea")
        

    # x, y = jugador.movimiento_personaje(key)
    # p.x = x
    # p.y = y
    # p.save()

    ok, buffer = cv2.imencode(".jpg", img)

    return HttpResponse(buffer.tobytes(), content_type="image/jpg")

def tablero(request):
    return render(request, "tablero.html")