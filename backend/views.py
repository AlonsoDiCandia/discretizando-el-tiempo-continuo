import os
import random
import json
import cv2
import numpy as np
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from backend.models import Personaje, PersonajeSeleccionado
from backend.generar_imagen.Jugador import Jugador

W = 1000
H = 500
PATH = os.getcwd()

# --- 1. FUNCIÓN PARA GENERAR EL LABERINTO ALEATORIO (Matriz) ---
def crear_matriz_laberinto(ancho_celdas, alto_celdas):
    w = ancho_celdas if ancho_celdas % 2 != 0 else ancho_celdas + 1
    h = alto_celdas if alto_celdas % 2 != 0 else alto_celdas + 1
    
    grid = [[1 for _ in range(w)] for _ in range(h)]
    
    def obtener_vecinos(x, y):
        vecinos = []
        direcciones = [(0, -2), (0, 2), (-2, 0), (2, 0)]
        for dx, dy in direcciones:
            nx, ny = x + dx, y + dy
            if 0 < nx < w - 1 and 0 < ny < h - 1:
                if grid[ny][nx] == 1:
                    vecinos.append((nx, ny, dx // 2, dy // 2))
        return vecinos

    stack = [(1, 1)]
    grid[1][1] = 0

    while stack:
        x, y = stack[-1]
        vecinos = obtener_vecinos(x, y)
        if vecinos:
            nx, ny, pdx, pdy = random.choice(vecinos)
            grid[y + pdy][x + pdx] = 0
            grid[ny][nx] = 0
            stack.append((nx, ny))
        else:
            stack.pop()
            
    return grid

# --- 2. FUNCIÓN PARA DIBUJAR LAS LÍNEAS DEL LABERINTO EN OPENCV ---
def dibujar_laberinto_en_imagen(img, grid):
    filas = len(grid)
    cols = len(grid[0])
    
    cell_w = W / cols
    cell_h = H / filas
    
    color_pared = (100, 200, 100) # Verde BGR
    
    for y in range(filas):
        for x in range(cols):
            if grid[y][x] == 1: # Si es pared, dibujamos el bloque/línea
                pt1 = (int(x * cell_w), int(y * cell_h))
                pt2 = (int((x + 1) * cell_w), int((y + 1) * cell_h))
                cv2.rectangle(img, pt1, pt2, color_pared, -1)


# --- ENDPOINT 1: Selección de personaje (Vista HTML) ---
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
    personaje_seleccionado = None
    if ps and ps.seleccionado:
        personaje_seleccionado = {
            "nombre": ps.seleccionado.nombre,
            "imagen_url": ps.seleccionado.imagen.url
        }
    
    return render(request, "seleccion_personaje.html", {
        "personajes": personajes, 
        "personaje_seleccionado": personaje_seleccionado
    })


# --- ENDPOINT 2: Guardar personaje seleccionado (POST) ---
@require_POST
def seleccionar_personaje(request, id):
    personaje = get_object_or_404(Personaje, id=id)
    ps = PersonajeSeleccionado.objects.first()
    if ps:
        ps.seleccionado = personaje
        ps.save()
    else:
        PersonajeSeleccionado.objects.create(seleccionado=personaje)
    return JsonResponse({"id": personaje.id, "nombre": personaje.nombre})


# --- ENDPOINT 3: Generador de imagen con OpenCV y laberinto aleatorio ---
def generar_imagen(request):
    ancho_celda = 30
    alto_celda = 15
    ps = PersonajeSeleccionado.objects.first()
    if not ps or not ps.seleccionado:
        return HttpResponse("No hay personaje seleccionado", status=400)
        
    p = ps.seleccionado
    jugador = Jugador(p, velocidad=int(W / ancho_celda))
    clave = request.GET.get("tecla", "")
    
    # Cargar imagen del personaje
    try:
        personaje = cv2.imread(PATH + p.imagen.url)
        personaje = cv2.resize(personaje, (int(W / ancho_celda) - 2, int(H / alto_celda) - 2))
    except Exception:
        personaje = np.zeros((40, 40, 3), dtype=np.uint8)

    # Generar un nuevo laberinto aleatorio en la sesión si no existe o se solicita reiniciar
    if 'laberinto' not in request.session or request.GET.get("nuevo_juego") == "1":
        request.session['laberinto'] = crear_matriz_laberinto(ancho_celda, alto_celda)
        request.session['pos_x'] = int(W / ancho_celda)  # Posición inicial segura
        request.session['pos_y'] = int(H / alto_celda)

    laberinto_grid = request.session['laberinto']

    # Recuperar posición actual
    x = request.session.get('pos_x', int(W / ancho_celda))
    y = request.session.get('pos_y', int(H / alto_celda))
    
    # Movimiento del personaje si se presionó tecla
    if clave:
        x, y = jugador.movimiento_personaje(clave)
        request.session['pos_x'] = x
        request.session['pos_y'] = y
        
    # Guardar cambios en el modelo del personaje como lo tenías planeado
    p.x = x
    p.y = y
    p.save()

    # Crear lienzo en blanco (Fondo Blanco)
    img = np.full((H, W, 3), 255, dtype=np.uint8)
    
    # Dibujar las líneas/paredes del laberinto aleatorio
    dibujar_laberinto_en_imagen(img, laberinto_grid)

    # Dibujar el tesoro/meta (opcional de referencia)
    tx, ty = 850, 250
    cv2.rectangle(img, (tx, ty), (tx + 40, ty + 40), (0, 0, 255), -1)

    # Dibujar personaje encima
    h_pers, w_pers = personaje.shape[:2]
    img[y:y+h_pers, x:x+w_pers] = personaje

    ok, buffer = cv2.imencode(".jpg", img)
    return HttpResponse(buffer.tobytes(), content_type="image/jpeg")


# --- ENDPOINT 4: Tablero de juego (Vista HTML) ---
def tablero(request):
    return render(request, "tablero.html")