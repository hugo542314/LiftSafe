# LiftSafe - Paso 3: pruebas de calculos.py con los valores de referencia del README.
# Se ejecuta con:  .\.venv\Scripts\python src\pruebas.py
import calculos


def comparar(nombre, calculado, esperado, tolerancia):
    """Compara un valor calculado con el esperado. Devuelve 0 si está bien y 1 si no."""
    if abs(calculado - esperado) <= tolerancia:
        print("  OK    ", nombre, "=", round(calculado, 3))
        return 0
    print("  ERROR ", nombre, "calculado", round(calculado, 3), "esperado", esperado)
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


total_errores = 0
total_errores = total_errores + probar_caso(
    "1. CG centrado", 2000, 0.0, 1.0, 2.0, 1.0, 13.873, 13.873, 45.0, 45.0)
total_errores = total_errores + probar_caso(
    "2. CG cerca de A", 2000, 0.0, 0.5, 2.0, 1.0, 16.452, 8.843, 63.43, 33.69)
total_errores = total_errores + probar_caso(
    "3. Simétrico a 30 grados", 1000, 0.0, 1.0, 2.0, 0.57735, 9.810, 9.810, 30.0, 30.0)
total_errores = total_errores + probar_caso(
    "4. Simétrico a 60 grados", 1000, 0.0, 1.0, 2.0, 1.73205, 5.664, 5.664, 60.0, 60.0)

print()
if total_errores == 0:
    print("Todas las pruebas son correctas.")
else:
    print("Comparaciones con error:", total_errores)