# LiftSafe - Paso 6: pruebas de calculos.py con los valores de referencia del README.
# Se ejecuta con:  .\.venv\Scripts\python src\pruebas.py
import calculos


def comparar(nombre, calculado, esperado, tolerancia):
    """Compara un valor calculado con el esperado. Devuelve 0 si está bien y 1 si no."""
    if abs(calculado - esperado) <= tolerancia:
        print("  OK    ", nombre, "=", round(calculado, 3))
        return 0
    print("  ERROR ", nombre, "calculado", round(calculado, 3), "esperado", esperado)
    return 1


def comparar_igual(nombre, calculado, esperado):
    """Compara dos valores que deben ser idénticos (textos, True/False). Devuelve 0 o 1."""
    if calculado == esperado:
        print("  OK    ", nombre, "=", repr(calculado))
        return 0
    print("  ERROR ", nombre, "calculado", repr(calculado), "esperado", repr(esperado))
    return 1


def probar_caso(nombre, masa_kg, x_a_m, x_g_m, x_b_m, altura_m,
                esperado_ta_kn, esperado_tb_kn, esperado_alfa, esperado_beta):
    """Calcula un caso completo y devuelve cuántas comparaciones han fallado."""
    print("Caso", nombre)
    peso_n = calculos.calcular_peso_n(masa_kg)
    ta_kn = calculos.calcular_tension_a_n(peso_n, x_a_m, x_g_m, x_b_m, altura_m) / 1000
    tb_kn = calculos.calcular_tension_b_n(peso_n, x_a_m, x_g_m, x_b_m, altura_m) / 1000
    alfa = calculos.calcular_angulo_a_grados(x_a_m, x_g_m, altura_m)
    beta = calculos.calcular_angulo_b_grados(x_g_m, x_b_m, altura_m)
    errores = 0
    errores = errores + comparar("T_A (kN)", ta_kn, esperado_ta_kn, 0.001)
    errores = errores + comparar("T_B (kN)", tb_kn, esperado_tb_kn, 0.001)
    errores = errores + comparar("alfa (grados)", alfa, esperado_alfa, 0.01)
    errores = errores + comparar("beta (grados)", beta, esperado_beta, 0.01)
    return errores


def probar_clasificacion():
    """Prueba los límites de los colores: lejos, justo en el límite y justo por encima."""
    print("Clasificación por porcentaje de capacidad")
    errores = 0
    errores = errores + comparar_igual("50 %", calculos.clasificar_eslinga(50.0), "verde")
    errores = errores + comparar_igual("80 %", calculos.clasificar_eslinga(80.0), "verde")
    errores = errores + comparar_igual("80.1 %", calculos.clasificar_eslinga(80.1), "ambar")
    errores = errores + comparar_igual("100 %", calculos.clasificar_eslinga(100.0), "ambar")
    errores = errores + comparar_igual("100.1 %", calculos.clasificar_eslinga(100.1), "rojo")
    return errores


def probar_validez():
    """Prueba cuándo un izado es válido: en los límites y justo fuera de ellos."""
    print("Validez de los datos")
    errores = 0
    errores = errores + comparar_igual(
        "datos normales", calculos.izado_valido(0.0, 1.0, 2.0, 1.0, 20000), True)
    errores = errores + comparar_igual(
        "CG justo en A", calculos.izado_valido(0.0, 0.0, 2.0, 1.0, 20000), True)
    errores = errores + comparar_igual(
        "CG justo en B", calculos.izado_valido(0.0, 2.0, 2.0, 1.0, 20000), True)
    errores = errores + comparar_igual(
        "CG fuera, junto a A", calculos.izado_valido(0.0, -0.1, 2.0, 1.0, 20000), False)
    errores = errores + comparar_igual(
        "CG fuera, junto a B", calculos.izado_valido(0.0, 2.1, 2.0, 1.0, 20000), False)
    errores = errores + comparar_igual(
        "A y B en el mismo punto", calculos.izado_valido(1.0, 1.0, 1.0, 1.0, 20000), False)
    errores = errores + comparar_igual(
        "altura 0", calculos.izado_valido(0.0, 1.0, 2.0, 0.0, 20000), False)
    errores = errores + comparar_igual(
        "capacidad 0", calculos.izado_valido(0.0, 1.0, 2.0, 1.0, 0), False)
    return errores


def probar_reparto():
    """Prueba qué eslinga carga más según la posición del CG."""
    print("Eslinga más cargada según el CG")
    errores = 0
    errores = errores + comparar_igual("CG en 1.0", calculos.eslinga_mas_cargada(0.0, 1.0, 2.0), "ninguna")
    errores = errores + comparar_igual("CG en 0.99", calculos.eslinga_mas_cargada(0.0, 0.99, 2.0), "ninguna")
    errores = errores + comparar_igual("CG en 0.9", calculos.eslinga_mas_cargada(0.0, 0.9, 2.0), "A")
    errores = errores + comparar_igual("CG en 1.1", calculos.eslinga_mas_cargada(0.0, 1.1, 2.0), "B")
    return errores


def probar_avisos():
    """Prueba los textos de aviso de cada eslinga."""
    print("Textos de aviso")
    errores = 0
    errores = errores + comparar_igual("50 %", calculos.redactar_aviso("A", 50.0), "")
    errores = errores + comparar_igual("80 %", calculos.redactar_aviso("A", 80.0), "")
    errores = errores + comparar_igual(
        "90 %", calculos.redactar_aviso("A", 90.0), "Eslinga A: poco margen (90 %)")
    errores = errores + comparar_igual(
        "110 %", calculos.redactar_aviso("B", 110.0), "Eslinga B: sobrecarga (110 %)")
    return errores


total_errores = 0
total_errores = total_errores + probar_caso(
    "1. CG centrado", 2000, 0.0, 1.0, 2.0, 1.0, 13.873, 13.873, 45.0, 45.0)
total_errores = total_errores + probar_caso(
    "2. CG cerca de A", 2000, 0.0, 0.5, 2.0, 1.0, 16.452, 8.843, 63.43, 33.69)
total_errores = total_errores + probar_caso(
    "3. Simétrico a 30 grados", 1000, 0.0, 1.0, 2.0, 0.57735, 9.810, 9.810, 30.0, 30.0)
total_errores = total_errores + probar_caso(
    "4. Simétrico a 60 grados", 1000, 0.0, 1.0, 2.0, 1.73205, 5.664, 5.664, 60.0, 60.0)
total_errores = total_errores + probar_clasificacion()
total_errores = total_errores + probar_validez()
total_errores = total_errores + probar_reparto()
total_errores = total_errores + probar_avisos()

print()
if total_errores == 0:
    print("Todas las pruebas son correctas.")
else:
    print("Comparaciones con error:", total_errores)