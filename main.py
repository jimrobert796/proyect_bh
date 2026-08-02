import pygame
import math
import sys
from src.jugador import Jugador
from src.enemigo import Enemigo

# --- Configuración base ---
ANCHO, ALTO = 480, 640  # proporción vertical típica de shmups/Touhou
FPS = 60

pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Bullet Hell - Prototipo")
reloj = pygame.time.Clock()

# --- Colores (placeholders, luego cambias por sprites) ---
BLANCO = (255, 255, 255)
NEGRO = (10, 10, 20)
AZUL = (100, 180, 255)
ROJO = (255, 80, 80)
AMARILLO = (255, 230, 100)

def main():
    jugador = Jugador()
    enemigo = Enemigo(ANCHO // 2, 100)
    jugando = True
    vidas = 3
    invulnerable_hasta = 0

    fuente = pygame.font.SysFont("consolas", 20)

    while jugando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jugando = False

        teclas = pygame.key.get_pressed()
        jugador.mover(teclas)
        jugador.actualizar_disparo(teclas)
        enemigo.actualizar(jugador)

        # Colisión: balas del enemigo contra el jugador
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual > invulnerable_hasta:
            for bala in enemigo.balas:
                if bala.colisiona_con(jugador):
                    vidas -= 1
                    invulnerable_hasta = tiempo_actual + 1500  # 1.5s de invulnerabilidad
                    enemigo.balas.remove(bala)
                    break

        # Colisión: balas del jugador contra el enemigo
        if enemigo.vivo:
            for bala in jugador.balas[:]:
                dist = math.hypot(bala.x - enemigo.x, bala.y - enemigo.y)
                if dist < (bala.radio + enemigo.radio):
                    enemigo.recibir_dano(5)
                    jugador.balas.remove(bala)

        # --- Dibujado ---
        pantalla.fill(NEGRO)
        jugador.dibujar(pantalla)
        enemigo.dibujar(pantalla)

        texto_vidas = fuente.render(f"Vidas: {vidas}", True, BLANCO)
        pantalla.blit(texto_vidas, (10, 10))

        if vidas <= 0:
            texto_gameover = fuente.render("GAME OVER", True, ROJO)
            pantalla.blit(texto_gameover, (ANCHO // 2 - 50, ALTO // 2))
        elif not enemigo.vivo:
            texto_victoria = fuente.render("¡ENEMIGO DERROTADO!", True, (100, 255, 100))
            pantalla.blit(texto_victoria, (ANCHO // 2 - 90, ALTO // 2))

        pygame.display.flip()
        reloj.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()