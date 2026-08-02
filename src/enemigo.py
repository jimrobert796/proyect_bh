import math
import pygame
from src.bala import Bala, ANCHO

ROJO = (255, 80, 80)
AMARILLO = (255, 230, 100)
VERDE = (100, 255, 100)


class Enemigo:
    """Enemigo fijo que dispara patrones. Los patrones son intercambiables:
    cada uno es solo un método 'disparar_X()' que agrega Balas a self.balas.
    La 'fase' decide qué patrón está activo y cuándo cambiar."""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radio = 20
        self.hp = 100
        self.vivo = True
        self.timer = 0            # frames transcurridos desde que empezó la fase actual
        self.balas = []

        # --- Sistema de fases ---
        # Cada fase define: cuánto dura (en frames), qué patrón usa, y cada cuántos
        # frames dispara ese patrón. Fácil de leer y de extender.
        self.fases = [
                    {"nombre": "spread", "duracion": 300, "intervalo": 20},
                    {"nombre": "anillo", "duracion": 180, "intervalo": 45},
                    {"nombre": "lluvia", "duracion": 240, "intervalo": 15},
                    {"nombre": "aimed_multiple", "duracion": 300, "intervalo": 40},
                ]
        self.indice_fase = 0
        self.angulo_espiral = 0  # estado propio del patrón espiral (rota con el tiempo)

    @property
    def fase_actual(self):
        return self.fases[self.indice_fase % len(self.fases)]

    def actualizar(self, jugador):
        if not self.vivo:
            return

        self.timer += 1
        fase = self.fase_actual

        # Cambiar de fase cuando se cumple la duración (vuelve a la primera al llegar al final,
        # así el enemigo repite el ciclo de patrones)
        if self.timer >= fase["duracion"]:
            self.timer = 0
            self.indice_fase += 1

        # Disparar según el patrón de la fase activa, respetando su intervalo
        if self.timer % fase["intervalo"] == 0:
            if fase["nombre"] == "spread":
                self.disparar_spread()
            elif fase["nombre"] == "espiral":
                self.disparar_espiral()
            elif fase["nombre"] == "aimed":
                self.disparar_aimed(jugador)
            elif fase["nombre"] == "anillo":
                self.disparar_anillo()
            elif fase["nombre"] == "lluvia":
                self.disparar_lluvia()
            elif fase["nombre"] == "aimed_multiple":
                self.disparar_aimed_multiple(jugador)

        for bala in self.balas:
            bala.actualizar()
        self.balas = [b for b in self.balas if not b.fuera_de_pantalla()]

    def recibir_dano(self, cantidad):
        self.hp -= cantidad
        if self.hp <= 0:
            self.hp = 0
            self.vivo = False

    # --- Patrones de bala ---
    # Cada uno solo calcula ángulos/velocidades distintos. Para agregar un patrón nuevo,
    # solo escribes un método como estos y lo registras en self.fases (ver README/chat).

    def disparar_spread(self, num_balas=7, angulo_total=100, velocidad=3):
        """Abanico de balas fijo, todas salen a la vez."""
        angulo_base = 90  # 90 = hacia abajo
        inicio = angulo_base - angulo_total // 2
        paso = angulo_total / (num_balas - 1) if num_balas > 1 else 0
        for i in range(num_balas):
            angulo = inicio + i * paso
            self.balas.append(Bala(self.x, self.y, angulo, velocidad))

    def disparar_espiral(self, velocidad=3):
        """Una sola bala por disparo, pero el ángulo rota un poco cada vez
        -> con el tiempo se dibuja una espiral completa."""
        self.balas.append(Bala(self.x, self.y, self.angulo_espiral, velocidad))
        self.angulo_espiral = (self.angulo_espiral + 15) % 360

    def disparar_aimed(self, jugador, velocidad=4):
        """Calcula el ángulo exacto hacia el jugador en el momento del disparo."""
        dx = jugador.x - self.x
        dy = jugador.y - self.y
        angulo = math.degrees(math.atan2(dy, dx))
        self.balas.append(Bala(self.x, self.y, angulo, velocidad, color=ROJO))

    def disparar_anillo(self, num_balas=16, velocidad=2.5):
        """360 grados completos de una sola vez -> efecto 'explosión' clásico."""
        paso = 360 / num_balas
        for i in range(num_balas):
            angulo = i * paso
            self.balas.append(Bala(self.x, self.y, angulo, velocidad))

    def disparar_doble_espiral(self, velocidad=3):
        """Dos brazos de espiral opuestos (180° de diferencia) -> se ve
        como una 'X' girando en vez de un solo brazo."""
        self.balas.append(Bala(self.x, self.y, self.angulo_espiral, velocidad))
        self.balas.append(Bala(self.x, self.y, self.angulo_espiral + 180, velocidad))
        self.angulo_espiral = (self.angulo_espiral + 10) % 360

    def disparar_espiral_multibrazo(self, brazos=4, velocidad=3):
        """Generaliza la espiral doble a N brazos repartidos uniformemente."""
        paso = 360 / brazos
        for i in range(brazos):
            angulo = self.angulo_espiral + i * paso
            self.balas.append(Bala(self.x, self.y, angulo, velocidad))
        self.angulo_espiral = (self.angulo_espiral + 8) % 360

    def disparar_ondas(self, velocidad=3, apertura=40):
        """Dos balas simétricas abriéndose en 'V' hacia abajo."""
        self.balas.append(Bala(self.x, self.y, 90 - apertura, velocidad))
        self.balas.append(Bala(self.x, self.y, 90 + apertura, velocidad))

    def disparar_aimed_multiple(self, jugador, num_balas=3, apertura=15, velocidad=4):
        """Como 'aimed', pero dispara varias balas alrededor del ángulo exacto
        hacia el jugador -> más difícil de esquivar que una sola bala apuntada."""
        dx = jugador.x - self.x
        dy = jugador.y - self.y
        angulo_centro = math.degrees(math.atan2(dy, dx))
        inicio = angulo_centro - apertura
        paso = (apertura * 2) / (num_balas - 1) if num_balas > 1 else 0
        for i in range(num_balas):
            angulo = inicio + i * paso
            self.balas.append(Bala(self.x, self.y, angulo, velocidad, color=ROJO))

    def disparar_lluvia(self, num_balas=5, velocidad=3):
        """Balas que caen desde posiciones X aleatorias por encima del enemigo,
        simulando 'lluvia' que cubre todo el ancho de pantalla."""
        import random
        for _ in range(num_balas):
            x_aleatorio = random.randint(20, ANCHO - 20)
            bala = Bala(x_aleatorio, self.y, 90, velocidad)
            self.balas.append(bala)

    def disparar_acelerada(self, velocidad_inicial=1, color=(200, 100, 255)):
        """Una bala 'aimed' que va acelerando con el tiempo. Necesita lógica
        extra en Bala (ver nota abajo) o se puede simular aumentando la
        velocidad base según self.timer."""
        velocidad = velocidad_inicial + (self.timer / 60)  # acelera con el tiempo transcurrido
        angulo = 90  # hacia abajo; combínalo con aimed si quieres que también apunte
        self.balas.append(Bala(self.x, self.y, angulo, velocidad, color=color))

    def disparar_espiral_alternada(self, velocidad=3):
        """Espiral que cambia de sentido de giro cada cierto tiempo,
        para que no sea 100% predecible."""
        direccion = 1 if (self.timer // 90) % 2 == 0 else -1
        self.balas.append(Bala(self.x, self.y, self.angulo_espiral, velocidad))
        self.angulo_espiral = (self.angulo_espiral + 12 * direccion) % 360

    def dibujar(self, superficie):
        if not self.vivo:
            return
        pygame.draw.circle(superficie, AMARILLO, (int(self.x), int(self.y)), self.radio)
        # Barra de HP simple arriba del enemigo
        ancho_barra = 60
        vida_restante = max(0, self.hp) / 100
        pygame.draw.rect(superficie, ROJO, (self.x - ancho_barra // 2, self.y - 35, ancho_barra, 6))
        pygame.draw.rect(superficie, VERDE,
                          (self.x - ancho_barra // 2, self.y - 35, ancho_barra * vida_restante, 6))
        for bala in self.balas:
            bala.dibujar(superficie)