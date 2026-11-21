# LiftSafe - Paso 2: dibujar la escena (carga, puntos de izado, CG, gancho y eslingas).
import pygame

# --- Datos de la escena en unidades reales (metros) ---------------------
x_a_m = 0.0              # posición del punto de izado A
x_b_m = 2.0              # posición del punto de izado B
x_g_m = 1.0              # posición del centro de gravedad (CG)
altura_gancho_m = 1.0    # altura del gancho sobre la carga
x_izq_carga_m = -0.2     # extremo izquierdo de la carga
largo_carga_m = 2.4
alto_carga_m = 0.6

# --- Ajustes de la ventana y del dibujo (píxeles) -----------------------
ANCHO_PX = 1000
ALTO_PX = 640
FOTOGRAMAS_POR_SEGUNDO = 60
PIXELES_POR_METRO = 200
ORIGEN_X_PX = 190        # columna de la ventana donde está x = 0 m
ORIGEN_Y_PX = 380        # fila de la ventana donde está el borde superior de la carga

# --- Colores (rojo, verde, azul) ----------------------------------------
COLOR_FONDO = (245, 245, 240)
COLOR_CARGA = (205, 205, 198)
COLOR_LINEA = (40, 40, 40)
COLOR_CG = (198, 40, 40)
COLOR_PUNTO = (31, 95, 168)

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

    # 2. Convertir de metros a píxeles. Los datos físicos están en metros;
    #    los píxeles solo se usan para dibujar.
    x_gancho_m = x_g_m  # el gancho queda en la vertical del CG
    x_a_px = ORIGEN_X_PX + x_a_m * PIXELES_POR_METRO
    x_b_px = ORIGEN_X_PX + x_b_m * PIXELES_POR_METRO
    x_g_px = ORIGEN_X_PX + x_gancho_m * PIXELES_POR_METRO
    x_gancho_px = ORIGEN_X_PX + x_gancho_m * PIXELES_POR_METRO
    # En la pantalla la y crece hacia abajo, por eso la altura se resta.
    y_gancho_px = ORIGEN_Y_PX - altura_gancho_m * PIXELES_POR_METRO
    y_g_px = ORIGEN_Y_PX + (alto_carga_m / 2) * PIXELES_POR_METRO
    x_carga_px = ORIGEN_X_PX + x_izq_carga_m * PIXELES_POR_METRO
    largo_carga_px = largo_carga_m * PIXELES_POR_METRO
    alto_carga_px = alto_carga_m * PIXELES_POR_METRO

    # 3. Dibujar el fotograma, de atrás hacia delante
    pantalla.fill(COLOR_FONDO)
    rectangulo_carga = (x_carga_px, ORIGEN_Y_PX, largo_carga_px, alto_carga_px)
    pygame.draw.rect(pantalla, COLOR_CARGA, rectangulo_carga)
    pygame.draw.rect(pantalla, COLOR_LINEA, rectangulo_carga, 3)
    pygame.draw.line(pantalla, COLOR_LINEA, (x_a_px, ORIGEN_Y_PX), (x_gancho_px, y_gancho_px), 4)
    pygame.draw.line(pantalla, COLOR_LINEA, (x_b_px, ORIGEN_Y_PX), (x_gancho_px, y_gancho_px), 4)
    pygame.draw.circle(pantalla, COLOR_PUNTO, (x_a_px, ORIGEN_Y_PX), 8)
    pygame.draw.circle(pantalla, COLOR_PUNTO, (x_b_px, ORIGEN_Y_PX), 8)
    pygame.draw.circle(pantalla, COLOR_LINEA, (x_gancho_px, y_gancho_px), 10, 4)
    pygame.draw.line(pantalla, COLOR_CG, (x_g_px - 10, y_g_px - 10), (x_g_px + 10, y_g_px + 10), 4)
    pygame.draw.line(pantalla, COLOR_CG, (x_g_px - 10, y_g_px + 10), (x_g_px + 10, y_g_px - 10), 4)

    # 4. Mostrar el fotograma y esperar para mantener 60 fotogramas por segundo
    pygame.display.flip()
    reloj.tick(FOTOGRAMAS_POR_SEGUNDO)

pygame.quit()