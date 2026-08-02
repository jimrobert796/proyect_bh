import pygame
from src.bala import Bala

ANCHO, ALTO = 480, 640
BLANCO = (255, 255, 255)
AZUL = (100, 180, 255)
AMARILLO = (255, 230, 100)


class Jugador:
    def __init__(self):
        self.x = ANCHO // 2
        self.y = ALTO - 80
        self.radio = 4          # hitbox pequeño (estilo Touhou: hitbox real es diminuto)
        self.radio_visual = 12  # el sprite se ve más grande que el hitbox real
        self.velocidad = 5
        self.velocidad_lenta = 2  # al mantener "shift" te mueves más lento (focus mode)

        # --- Disparo ---
        self.balas = []
        self.cooldown_disparo = 6   # frames entre disparo y disparo (menor = más rápido)
        self.contador_cooldown = 0

    def mover(self, teclas):
        vel = self.velocidad
        if teclas[pygame.K_LSHIFT]:
            vel = self.velocidad_lenta

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.x -= vel
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.x += vel
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            self.y -= vel
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            self.y += vel

        # Mantener al jugador dentro de la pantalla
        self.x = max(self.radio_visual, min(ANCHO - self.radio_visual, self.x))
        self.y = max(self.radio_visual, min(ALTO - self.radio_visual, self.y))

    def actualizar_disparo(self, teclas):
        # Cooldown baja cada frame; cuando llega a 0 y la tecla está presionada, dispara
        if self.contador_cooldown > 0:
            self.contador_cooldown -= 1

        disparando = teclas[pygame.K_z] or teclas[pygame.K_SPACE]
        if disparando and self.contador_cooldown == 0:
            # Ángulo 270 = hacia arriba en este sistema de coordenadas (y crece hacia abajo)
            self.balas.append(Bala(self.x, self.y, 270, 8, color=AMARILLO, radio=4))
            self.contador_cooldown = self.cooldown_disparo

        for bala in self.balas:
            bala.actualizar()
        self.balas = [b for b in self.balas if not b.fuera_de_pantalla()]

    def dibujar(self, superficie):
        pygame.draw.circle(superficie, AZUL, (int(self.x), int(self.y)), self.radio_visual)
        # Hitbox real visible solo si mantienes shift (como en los juegos originales)
        pygame.draw.circle(superficie, BLANCO, (int(self.x), int(self.y)), self.radio, 1)
        for bala in self.balas:
            bala.dibujar(superficie)