# LiftSafe - Paso 1: abrir una ventana de Pygame con su bucle principal.
import pygame

# --- Valores iniciales --------------------------------------------------
ANCHO_PX = 1000
ALTO_PX = 640
COLOR_FONDO = (245, 245, 240)  # (rojo, verde, azul), cada uno de 0 a 255
FOTOGRAMAS_POR_SEGUNDO = 60

pygame.init()
pantalla = pygame.display.set_mode((ANCHO_PX, ALTO_PX))
pygame.display.set_caption("LiftSafe")
reloj = pygame.time.Clock()

# --- Bucle principal ----------------------------------------------------
ejecutando = True
while ejecutando:
    # 1. Leer los eventos (clics, teclas, cerrar la ventana...)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # 2. Dibujar el fotograma
    pantalla.fill(COLOR_FONDO)

    # 3. Mostrar el fotograma y esperar para mantener 60 fotogramas por segundo
    pygame.display.flip()
    reloj.tick(FOTOGRAMAS_POR_SEGUNDO)

pygame.quit()