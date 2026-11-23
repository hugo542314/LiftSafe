# LiftSafe - Paso 4: cálculos de estática para un izado con dos eslingas.
# Este archivo no usa Pygame: solo hace cuentas.
# Unidades: masa en kg, posiciones y alturas en m, fuerzas en N, ángulos en grados.
import math

GRAVEDAD_M_S2 = 9.81
UMBRAL_AMBAR_PORCENTAJE = 80.0    # a partir de aquí se avisa de que queda poco margen
UMBRAL_ROJO_PORCENTAJE = 100.0    # por encima, la eslinga supera su capacidad


def calcular_peso_n(masa_kg):
    """Peso de la carga en newtons: masa por gravedad."""
    return masa_kg * GRAVEDAD_M_S2


def calcular_reaccion_a_n(peso_n, x_a_m, x_g_m, x_b_m):
    """Parte vertical de la fuerza de la eslinga A (regla de la palanca)."""
    distancia_b_m = x_b_m - x_g_m
    largo_m = x_b_m - x_a_m
    return peso_n * distancia_b_m / largo_m


def calcular_reaccion_b_n(peso_n, x_a_m, x_g_m, x_b_m):
    """Parte vertical de la fuerza de la eslinga B (regla de la palanca)."""
    distancia_a_m = x_g_m - x_a_m
    largo_m = x_b_m - x_a_m
    return peso_n * distancia_a_m / largo_m


def calcular_fuerza_horizontal_n(peso_n, x_a_m, x_g_m, x_b_m, altura_m):
    """Parte horizontal de la fuerza de las eslingas (es la misma en las dos)."""
    distancia_a_m = x_g_m - x_a_m
    distancia_b_m = x_b_m - x_g_m
    largo_m = x_b_m - x_a_m
    return peso_n * distancia_a_m * distancia_b_m / (altura_m * largo_m)


def calcular_tension_a_n(peso_n, x_a_m, x_g_m, x_b_m, altura_m):
    """Tensión total de la eslinga A: se combinan su parte vertical y la horizontal."""
    vertical_n = calcular_reaccion_a_n(peso_n, x_a_m, x_g_m, x_b_m)
    horizontal_n = calcular_fuerza_horizontal_n(peso_n, x_a_m, x_g_m, x_b_m, altura_m)
    return math.sqrt(horizontal_n ** 2 + vertical_n ** 2)


def calcular_tension_b_n(peso_n, x_a_m, x_g_m, x_b_m, altura_m):
    """Tensión total de la eslinga B: se combinan su parte vertical y la horizontal."""
    vertical_n = calcular_reaccion_b_n(peso_n, x_a_m, x_g_m, x_b_m)
    horizontal_n = calcular_fuerza_horizontal_n(peso_n, x_a_m, x_g_m, x_b_m, altura_m)
    return math.sqrt(horizontal_n ** 2 + vertical_n ** 2)


def calcular_angulo_a_grados(x_a_m, x_g_m, altura_m):
    """Ángulo de la eslinga A con la horizontal, en grados."""
    distancia_a_m = x_g_m - x_a_m
    return math.degrees(math.atan2(altura_m, distancia_a_m))


def calcular_angulo_b_grados(x_g_m, x_b_m, altura_m):
    """Ángulo de la eslinga B con la horizontal, en grados."""
    distancia_b_m = x_b_m - x_g_m
    return math.degrees(math.atan2(altura_m, distancia_b_m))


def calcular_porcentaje_capacidad(tension_n, capacidad_n):
    """Qué porcentaje de su capacidad está usando una eslinga."""
    return tension_n / capacidad_n * 100


def clasificar_eslinga(porcentaje):
    """Devuelve 'verde', 'ambar' o 'rojo' según el porcentaje de capacidad usado."""
    if porcentaje > UMBRAL_ROJO_PORCENTAJE:
        return "rojo"
    elif porcentaje > UMBRAL_AMBAR_PORCENTAJE:
        return "ambar"
    return "verde"