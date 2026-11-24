# LiftSafe - Paso 5: programa interactivo (botones + y - con el ratón, y teclado).
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

# --- Límites y pasos de los controles -----------------------------------
MASA_MIN_KG = 500
MASA_MAX_KG = 5000
PASO_MASA_KG = 250
PASO_CG_M = 0.1          # el CG solo se mueve entre A y B
ALTURA_MIN_M = 0.2
ALTURA_MAX_M = 1.6
PASO_ALTURA_M = 0.1
CAPACIDAD_MIN_KN = 5.0
CAPACIDAD_MAX_KN = 60.0
PASO_CAPACIDAD_KN = 5.0

# --- Ajustes de la ventana y del dibujo (píxeles) -----------------------
ANCHO_PX = 1000
ALTO_PX = 640
FOTOGRAMAS_POR_SEGUNDO = 60
PIXELES_POR_METRO = 200
ORIGEN_X_PX = 190        # columna de la ventana donde está x = 0 m
ORIGEN_Y_PX = 380        # fila de la ventana donde está el borde superior de la carga
PANEL_X_PX = 690         # columna donde empieza el texto de los paneles
CONTROLES_Y0_PX = 66     # fila de la ventana donde está el primer control
ALTO_FILA_PX = 40        # separación entre controles
LADO_BOTON_PX = 30
BOTON_MENOS_X_PX = 905
BOTON_MAS_X_PX = 945

# --- Colores (rojo, verde, azul) ----------------------------------------
COLOR_FONDO = (245, 245, 240)
COLOR_PANEL = (255, 255, 255)
COLOR_CARGA = (205, 205, 198)
COLOR_LINEA = (40, 40, 40)
COLOR_TEXTO = (40, 40, 40)
COLOR_GRIS = (110, 110, 110)
COLOR_BOTON = (235, 235, 230)
COLOR_SELECCION = (222, 235, 250)
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


def limitar(valor, minimo, maximo):
    """Devuelve el valor, pero sin salirse del intervalo entre minimo y maximo."""
    return max(minimo, min(maximo, valor))


def y_de_fila(fila):
    """Fila de la ventana (en píxeles) donde está el control número 'fila'."""
    return CONTROLES_Y0_PX + fila * ALTO_FILA_PX


def rectangulo_boton(fila, es_mas):
    """Rectángulo del botón - (es_mas = False) o + (es_mas = True) de un control."""
    y_px = y_de_fila(fila) - 4
    if es_mas:
        return pygame.Rect(BOTON_MAS_X_PX, y_px, LADO_BOTON_PX, LADO_BOTON_PX)
    return pygame.Rect(BOTON_MENOS_X_PX, y_px, LADO_BOTON_PX, LADO_BOTON_PX)


def dibujar_boton(superficie, rectangulo, es_mas):
    """Dibuja un botón cuadrado con el signo - o + en su interior."""
    pygame.draw.rect(superficie, COLOR_BOTON, rectangulo)
    pygame.draw.rect(superficie, COLOR_LINEA, rectangulo, 2)
    centro_x = rectangulo.centerx
    centro_y = rectangulo.centery
    pygame.draw.line(superficie, COLOR_LINEA, (centro_x - 7, centro_y), (centro_x + 7, centro_y), 3)
    if es_mas:
        pygame.draw.line(superficie, COLOR_LINEA, (centro_x, centro_y - 7), (centro_x, centro_y + 7), 3)


pygame.init()
pygame.key.set_repeat(300, 50)  # al mantener una tecla pulsada, se repite
pantalla = pygame.display.set_mode((ANCHO_PX, ALTO_PX))
pygame.display.set_caption("LiftSafe")
reloj = pygame.time.Clock()
fuente = pygame.font.SysFont("arial", 22)
fuente_control = pygame.font.SysFont("arial", 20)
fuente_pequena = pygame.font.SysFont("arial", 16)
fuente_negrita = pygame.font.SysFont("arial", 24, bold=True)

# --- Bucle principal ----------------------------------------------------
seleccionado = 0         # control elegido con el teclado: 0 masa, 1 CG, 2 altura, 3 capacidad
ejecutando = True
while ejecutando:
    # 1. Leer los eventos (cerrar, clics, teclas)
    parametro = -1       # control que se cambia en este fotograma (-1 = ninguno)
    direccion = 0        # -1 = bajar el valor, 1 = subirlo
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            for fila in range(4):
                if rectangulo_boton(fila, False).collidepoint(evento.pos):
                    seleccionado = fila
                    parametro = fila
                    direccion = -1
                if rectangulo_boton(fila, True).collidepoint(evento.pos):
                    seleccionado = fila
                    parametro = fila
                    direccion = 1
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                seleccionado = max(0, seleccionado - 1)
            elif evento.key == pygame.K_DOWN:
                seleccionado = min(3, seleccionado + 1)
            elif evento.key == pygame.K_LEFT:
                parametro = seleccionado
                direccion = -1
            elif evento.key == pygame.K_RIGHT:
                parametro = seleccionado
                direccion = 1

    # 2. Actualizar el valor que se haya cambiado, siempre dentro de sus límites
    if parametro == 0:
        masa_kg = limitar(masa_kg + direccion * PASO_MASA_KG, MASA_MIN_KG, MASA_MAX_KG)
    elif parametro == 1:
        x_g_m = round(limitar(x_g_m + direccion * PASO_CG_M, x_a_m, x_b_m), 1)
    elif parametro == 2:
        altura_gancho_m = round(
            limitar(altura_gancho_m + direccion * PASO_ALTURA_M, ALTURA_MIN_M, ALTURA_MAX_M), 1)
    elif parametro == 3:
        capacidad_kn = limitar(
            capacidad_kn + direccion * PASO_CAPACIDAD_KN, CAPACIDAD_MIN_KN, CAPACIDAD_MAX_KN)

    # 3. Calcular con las funciones de calculos.py (todo en unidades del SI)
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

    # 4. Convertir de metros a píxeles (los píxeles solo se usan para dibujar)
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

    # 5. Dibujar el fotograma, de atrás hacia delante
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

    # Panel de controles
    pygame.draw.rect(pantalla, COLOR_PANEL, (670, 20, 310, 250))
    pygame.draw.rect(pantalla, COLOR_LINEA, (670, 20, 310, 250), 2)
    escribir(pantalla, fuente_negrita, "Controles", PANEL_X_PX, 30, COLOR_TEXTO)
    pygame.draw.rect(pantalla, COLOR_SELECCION, (678, y_de_fila(seleccionado) - 6, 294, 36))
    escribir(pantalla, fuente_control, f"Masa: {masa_kg} kg", PANEL_X_PX, y_de_fila(0), COLOR_TEXTO)
    escribir(pantalla, fuente_control, f"Posición CG: {x_g_m:.1f} m", PANEL_X_PX, y_de_fila(1), COLOR_TEXTO)
    escribir(pantalla, fuente_control, f"Altura gancho: {altura_gancho_m:.1f} m", PANEL_X_PX, y_de_fila(2), COLOR_TEXTO)
    escribir(pantalla, fuente_control, f"Capacidad: {capacidad_kn:.1f} kN", PANEL_X_PX, y_de_fila(3), COLOR_TEXTO)
    for fila in range(4):
        dibujar_boton(pantalla, rectangulo_boton(fila, False), False)
        dibujar_boton(pantalla, rectangulo_boton(fila, True), True)
    escribir(pantalla, fuente_pequena, "Flechas arriba/abajo: elegir control", PANEL_X_PX, 232, COLOR_GRIS)
    escribir(pantalla, fuente_pequena, "Flechas izquierda/derecha: cambiar", PANEL_X_PX, 250, COLOR_GRIS)

    # Panel de resultados (los números se convierten de N a kN solo para mostrarlos)
    pygame.draw.rect(pantalla, COLOR_PANEL, (670, 282, 310, 250))
    pygame.draw.rect(pantalla, COLOR_LINEA, (670, 282, 310, 250), 2)
    escribir(pantalla, fuente_negrita, "Resultados", PANEL_X_PX, 292, COLOR_TEXTO)

    pygame.draw.rect(pantalla, color_a, (PANEL_X_PX, 336, 18, 18))
    escribir(pantalla, fuente_negrita, "Eslinga A", PANEL_X_PX + 30, 332, COLOR_TEXTO)
    escribir(pantalla, fuente, f"{tension_a_n / 1000:.2f} kN  ({porcentaje_a:.0f} % de uso)", PANEL_X_PX, 362, COLOR_TEXTO)
    escribir(pantalla, fuente, f"Ángulo: {angulo_a_grados:.1f}°", PANEL_X_PX, 388, COLOR_TEXTO)

    pygame.draw.rect(pantalla, color_b, (PANEL_X_PX, 440, 18, 18))
    escribir(pantalla, fuente_negrita, "Eslinga B", PANEL_X_PX + 30, 436, COLOR_TEXTO)
    escribir(pantalla, fuente, f"{tension_b_n / 1000:.2f} kN  ({porcentaje_b:.0f} % de uso)", PANEL_X_PX, 466, COLOR_TEXTO)
    escribir(pantalla, fuente, f"Ángulo: {angulo_b_grados:.1f}°", PANEL_X_PX, 492, COLOR_TEXTO)

    # 6. Mostrar el fotograma y esperar para mantener 60 fotogramas por segundo
    pygame.display.flip()
    reloj.tick(FOTOGRAMAS_POR_SEGUNDO)

pygame.quit()