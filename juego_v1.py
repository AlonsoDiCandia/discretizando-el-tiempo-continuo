import cv2
import numpy as np
import os
import django

# 1. Configura la variable de entorno apuntando al settings de tu proyecto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'juego.settings')

# 2. Inicializa Django
django.setup()

from backend.models import Personaje

def hay_colision(xA, yA, anchoA, altoA, xB, yB, anchoB, altoB):
    solapan_en_x = (xA < xB + anchoB) and (xB < xA + anchoA)
    solapan_en_y = (yA < yB + altoB) and (yB < yA + altoA)
    return solapan_en_x and solapan_en_y

p = Personaje.objects.first()
print(p.x, p.y)

W = 1000
H = 500


personaje = cv2.imread("personaje.png")
personaje = cv2.resize(personaje, (100,100))

# Inicio personaje
x,y = p.x, p.y
speed = 25

tesoro = cv2.imread("tesoro.jpg")
tesoro = cv2.resize(tesoro, (100,100))

# Inicio tesoro
tx, ty = 600, 250

while True:
    img = np.full((H, W, 3), 255, dtype=np.uint8)
    # Personaje a la imagen
    img[y:y+personaje.shape[0], x:x+personaje.shape[1]] = personaje
    
    img[ty:ty+tesoro.shape[0], tx:tx+tesoro.shape[1]] = tesoro
    
    cv2.circle(img, (x+personaje.shape[1], y), 2, (0,0,255), 2)
    cv2.imshow("Juevo v1", img)

    if (cv2.waitKey(500) & 0xFF) == ord("q"):
        break
    elif (cv2.waitKey(500) & 0xFF) == ord("d"):
        x = x + speed
    elif (cv2.waitKey(500) & 0xFF) == ord("a"):
        x = x - speed
    elif (cv2.waitKey(500) & 0xFF) == ord("w"):
        y = y - speed
    elif (cv2.waitKey(500) & 0xFF) == ord("s"):
        y = y + speed

    p.x = x
    p.y = y
    p.save()
       
    c1 = y, x
    c2 = y, x + personaje.shape[1]
    c3 = y + personaje.shape[0], x
    c4 = y + personaje.shape[0], x + personaje.shape[1]
    
    if hay_colision(x,y, personaje.shape[0], personaje.shape[1], tx,ty, tesoro.shape[0], tesoro.shape[1]):
        print("Colision")