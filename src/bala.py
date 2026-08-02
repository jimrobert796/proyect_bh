import math
import pygame

# --- Configuración compartida (podrías moverla a un config.py si crece) ---
ANCHO, ALTO = 480, 640


class Bala:
    def __init__(self, x, y, angulo_grados, velocidad, color=(255, 80, 80), radio=5):
        self.x = x
        self.y = y
        angulo = math.radians(angulo_grados)
        self.vx = math.cos(angulo) * velocidad
        self.vy = math.sin(angulo) * velocidad
        self.color = color
        self.radio = radio

    def actualizar(self):
        self.x += self.vx
        self.y += self.vy

    def fuera_de_pantalla(self):
        margen = 20
        return (self.x < -margen or self.x > ANCHO + margen or
                self.y < -margen or self.y > ALTO + margen)

    def dibujar(self, superficie):
        pygame.draw.circle(superficie, self.color, (int(self.x), int(self.y)), self.radio)

    def colisiona_con(self, entidad):
        dist = math.hypot(self.x - entidad.x, self.y - entidad.y)
        return dist < (self.radio + entidad.radio)