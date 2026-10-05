

class Personaje:
    def __init__(self, personaje_db):
        self.x = personaje_db.x
        self.y = personaje_db.y
        self.velocidad = personaje_db.velocidad
        
        
    def movimiento_personaje(self, key):
        x = self.x
        y = self.y
        
        print(key)
        
        if key == ord("d"):
            x = x + self.velocidad
        elif key == ord("a"):
            x = x - self.velocidad
        elif key == ord("w"):
            y = y - self.velocidad
        elif key == ord("s"):
            y = y + self.velocidad
            
        self.x = x
        self.y = y

        return x, y