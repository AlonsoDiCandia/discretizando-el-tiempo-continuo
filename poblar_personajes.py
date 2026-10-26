import os
from pathlib import Path
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'juego.settings')
django.setup()

from backend.models import Personaje

BASE_DIR = Path(__file__).resolve().parent

PERSONAJES = {
    "pepe": "personaje.png",
    "samael": "unnamed.jpg",
    "Don M": "dxcmkj8eb7yic_600.jpg",
}

for nombre, archivo in PERSONAJES.items():
    if not (BASE_DIR / "static" / archivo).exists():
        raise FileNotFoundError(f"Falta static/{archivo}")

    Personaje.objects.update_or_create(
        nombre=nombre,
        defaults={
            "x": 50,
            "y": 50,
            "velocidad": 25,
            "imagen": (Path("static") / archivo).as_posix(),
        },
    )