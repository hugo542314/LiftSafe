# LiftSafe - Paso 4: unir el cálculo (calculos.py) con el dibujo y los resultados.
import pygame
import calculos

# --- Datos de la escena en unidades reales (kg, m, kN) ------------------
masa_kg = 2000
x_a_m = 0.0              # posición del punto de izado A
x_b_m = 2.0              # posición del punto de izado B
x_g_m = 1.0              # posición del centro de gravedad (CG)
altura_gancho_m = 1.0    # altura del gancho sobre la carga
capacidad_kn = 20.0      # capacidad de cada eslinga (la misma para las dos)
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
PANEL_X_PX = 690         # columna donde empieza el texto del panel de resultados

# --- Colores (rojo, verde, azul) ----------------------------------------
COLOR_FONDO = (245, 245, 240)
COLOR_PANEL = (255, 255, 255)
COLOR_CARGA = (205, 205, 198)
COLOR_LINEA = (40, 40, 40)
COLOR_TEXTO = (40, 40, 40)
COLOR_CG = (198, 40, 40)
COLOR_PUNTO = (31, 95, 168)
COLOR_VERDE = (46, 125, 50)
COLOR_AMBAR = (230, 145, 0)
COLOR_ROJO = (198, 40, 40)


def color_de_estado(estado):
    """Devuelve el color que corresponde al estado de una eslinga."""
    if estado == "verde":
        return COLOR_VERDE
    elif estado == "ambar":
        return COLOR_AMBAR
    return COLOR_ROJO


def escribir(superficie, fuente, texto, x_px, y_px, color):
    """Dibuja un texto con su esquina superior izquierda en (x_px, y_px)."""
    imagen_texto = fuente.render(texto, True, color)
    superficie.blit(imagen_texto, (x_px, y_px))


pygame.init()
pantalla = pygame.display.set_mode((ANCHO_PX, ALTO_PX))
pygame.display.set_caption("LiftSafe")
reloj = pygame.time.Clock()
fuente = pygame.font.SysFont("arial", 22)
fuente_negrita = pygame.font.SysFont("arial", 24, bold=True)

# --- Bucle principal ----------------------------------------------------
ejecutando = True
while ejecutando:
    # 1. Leer los eventos (clics, teclas, cerrar la ventana...)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # 2. Calcular con las funciones de calculos.py (todo en unidades del SI)
    peso_n = calculos.calcular_peso_n(masa_kg)
    tension_a_n = calculos.calcular_tension_a_n(peso_n, x_a_m, x_g_m, x_b_m, altura_gancho_m)
    tension_b_n = calculos.calcular_tension_b_n(peso_n, x_a_m, x_g_m, x_b_m, altura_gancho_m)
    angulo_a_grados = calculos.calcular_angulo_a_grados(x_a_m, x_g_m, altura_gancho_m)
    angulo_b_grados = calculos.calcular_angulo_b_grados(x_g_m, x_b_m, altura_gancho_m)
    capacidad_n = capacidad_kn * 1000
    porcentaje_a = calculos.calcular_porcentaje_capacidad(tension_a_n, capacidad_n)
    porcentaje_b = calculos.calcular_porcentaje_capacidad(tension_b_n, capacidad_n)
    color_a = color_de_estado(calculos.clasificar_eslinga(porcentaje_a))
    color_b = color_de_estado(calculos.clasificar_eslinga(porcentaje_b))

    # 3. Convertir de metros a píxeles (los píxeles solo se usan para dibujar)
    x_gancho_m = x_g_m  # el gancho queda en la vertical del CG
    x_a_px = ORIGEN_X_PX + x_a_m * PIXELES_POR_METRO
    x_b_px = ORIGEN_X_PX + x_b_m * PIXELES_POR_METRO
    x_g_px = ORIGEN_X_PX + x_g_m * PIXELES_POR_METRO
    x_gancho_px = ORIGEN_X_PX + x_gancho_m * PIXELES_POR_METRO
    # En la pantalla la y crece hacia abajo, por eso la altura se resta.
    y_gancho_px = ORIGEN_Y_PX - altura_gancho_m * PIXELES_POR_METRO
    y_g_px = ORIGEN_Y_PX + (alto_carga_m / 2) * PIXELES_POR_METRO
    x_carga_px = ORIGEN_X_PX + x_izq_carga_m * PIXELES_POR_METRO
    largo_carga_px = largo_carga_m * PIXELES_POR_METRO
    alto_carga_px = alto_carga_m * PIXELES_POR_METRO

    # 4. Dibujar el fotograma, de atrás hacia delante
    pantalla.fill(COLOR_FONDO)
    rectangulo_carga = (x_carga_px, ORIGEN_Y_PX, largo_carga_px, alto_carga_px)
    pygame.draw.rect(pantalla, COLOR_CARGA, rectangulo_carga)
    pygame.draw.rect(pantalla, COLOR_LINEA, rectangulo_carga, 3)
    pygame.draw.line(pantalla, color_a, (x_a_px, ORIGEN_Y_PX), (x_gancho_px, y_gancho_px), 5)
    pygame.draw.line(pantalla, color_b, (x_b_px, ORIGEN_Y_PX), (x_gancho_px, y_gancho_px), 5)
    pygame.draw.circle(pantalla, COLOR_PUNTO, (x_a_px, ORIGEN_Y_PX), 8)
    pygame.draw.circle(pantalla, COLOR_PUNTO, (x_b_px, ORIGEN_Y_PX), 8)
    pygame.draw.circle(pantalla, COLOR_LINEA, (x_gancho_px, y_gancho_px), 10, 4)
    pygame.draw.line(pantalla, COLOR_CG, (x_g_px - 10, y_g_px - 10), (x_g_px + 10, y_g_px + 10), 4)
    pygame.draw.line(pantalla, COLOR_CG, (x_g_px - 10, y_g_px + 10), (x_g_px + 10, y_g_px - 10), 4)
    escribir(pantalla, fuente_negrita, "A", x_a_px - 8, ORIGEN_Y_PX + 14, COLOR_TEXTO)
    escribir(pantalla, fuente_negrita, "B", x_b_px - 8, ORIGEN_Y_PX + 14, COLOR_TEXTO)
    escribir(pantalla, fuente_negrita, "CG", x_g_px + 16, y_g_px - 12, COLOR_CG)

    # Panel de resultados (los números se convierten de N a kN solo para mostrarlos)
    pygame.draw.rect(pantalla, COLOR_PANEL, (670, 20, 310, 600))
    pygame.draw.rect(pantalla, COLOR_LINEA, (670, 20, 310, 600), 2)
    escribir(pantalla, fuente_negrita, "Resultados", PANEL_X_PX, 40, COLOR_TEXTO)
    escribir(pantalla, fuente, f"Masa: {masa_kg} kg", PANEL_X_PX, 90, COLOR_TEXTO)
    escribir(pantalla, fuente, f"Capacidad: {capacidad_kn:.1f} kN", PANEL_X_PX, 120, COLOR_TEXTO)

    pygame.draw.rect(pantalla, color_a, (PANEL_X_PX, 178, 18, 18))
    escribir(pantalla, fuente_negrita, "Eslinga A", PANEL_X_PX + 30, 175, COLOR_TEXTO)
    escribir(pantalla, fuente, f"Tensión: {tension_a_n / 1000:.2f} kN", PANEL_X_PX, 210, COLOR_TEXTO)
    escribir(pantalla, fuente, f"Capacidad usada: {porcentaje_a:.0f} %", PANEL_X_PX, 238, COLOR_TEXTO)
    escribir(pantalla, fuente, f"Ángulo: {angulo_a_grados:.1f}°", PANEL_X_PX, 266, COLOR_TEXTO)

    pygame.draw.rect(pantalla, color_b, (PANEL_X_PX, 328, 18, 18))
    escribir(pantalla, fuente_negrita, "Eslinga B", PANEL_X_PX + 30, 325, COLOR_TEXTO)
    escribir(pantalla, fuente, f"Tensión: {tension_b_n / 1000:.2f} kN", PANEL_X_PX, 360, COLOR_TEXTO)
    escribir(pantalla, fuente, f"Capacidad usada: {porcentaje_b:.0f} %", PANEL_X_PX, 388, COLOR_TEXTO)
    escribir(pantalla, fuente, f"Ángulo: {angulo_b_grados:.1f}°", PANEL_X_PX, 416, COLOR_TEXTO)

    # 5. Mostrar el fotograma y esperar para mantener 60 fotogramas por segundo
    pygame.display.flip()
    reloj.tick(FOTOGRAMAS_POR_SEGUNDO)

pygame.quit()