import time
from datos import canales_publicitarios, presupuesto_total_campana, reglas_sinergia
from fuerza_bruta import optimizar_gasto
from programacion_dinamica import optimizar_gasto_programacion_dinamica

import time  # Para medir el tiempo


# Esta función muestra los resultados de un algoritmo
def mostrar_resultados(nombre_algoritmo, resultado, tiempo):
    print(f"\n=== RESULTADOS DEL ALGORITMO {nombre_algoritmo.upper()} ===")
    print(f"Tiempo de ejecución: {tiempo:.6f} segundos")

    print("\nInversiones realizadas:")
    for inversion in resultado["inversiones"]:
        print(f"Canal: {inversion['id_canal']}")
        print(f"  Paquete: {inversion['id_paquete_seleccionado']}")
        print(f"  Costo: {inversion['costo_del_paquete_seleccionado']}")
        print(f"  Retorno final: {inversion['retorno_final_del_canal']}")
        print("-" * 30)

    print("\nResumen global:")
    resumen = resultado["resumen_global"]
    print(f"Costo total invertido: {resumen['costo_total_invertido_calculado']}")
    print(f"Retorno total esperado: {resumen['retorno_total_final_esperado_calculado']}")
    print(f"Presupuesto restante: {resumen['presupuesto_restante']}")


# Esta función compara ambos algoritmos
def comparar_algoritmos():
    print("Optimizador de Gasto Publicitario - Comparación de Algoritmos")
    print("=" * 60)

    # Ejecutamos Fuerza Bruta
    print("\nEjecutando algoritmo de Fuerza Bruta...")
    inicio_fb = time.time()
    resultado_fb = optimizar_gasto(canales_publicitarios, presupuesto_total_campana, reglas_sinergia)
    fin_fb = time.time()
    tiempo_fb = fin_fb - inicio_fb

    mostrar_resultados("Fuerza Bruta", resultado_fb, tiempo_fb)

    # Ejecutamos Programación Dinámica
    print("\nEjecutando algoritmo de Programación Dinámica...")
    inicio_pd = time.time()
    resultado_pd = optimizar_gasto_programacion_dinamica(canales_publicitarios, presupuesto_total_campana,
                                                         reglas_sinergia)
    fin_pd = time.time()
    tiempo_pd = fin_pd - inicio_pd

    mostrar_resultados("Programación Dinámica", resultado_pd, tiempo_pd)

    # Obtenemos los retornos de ambos
    retorno_fb = resultado_fb["resumen_global"]["retorno_total_final_esperado_calculado"]
    retorno_pd = resultado_pd["resumen_global"]["retorno_total_final_esperado_calculado"]

    # Mostramos la comparación
    print("\n=== COMPARACIÓN DE ALGORITMOS ===")
    print(f"Fuerza Bruta:")
    print(f"  Tiempo: {tiempo_fb:.6f} segundos")
    print(f"  Retorno: {retorno_fb}")

    print(f"\nProgramación Dinámica:")
    print(f"  Tiempo: {tiempo_pd:.6f} segundos")
    print(f"  Retorno: {retorno_pd}")

    # Calculamos mejora en porcentaje
    if tiempo_fb > 0:
        mejora = ((tiempo_fb - tiempo_pd) / tiempo_fb) * 100
        print(f"\nMejora en tiempo: {mejora:.2f}%")

    print(f"Diferencia en retorno: {retorno_pd - retorno_fb}")

    # Verificamos si los resultados son iguales
    if abs(retorno_pd - retorno_fb) < 0.001:
        print("\nLos algoritmos encontraron el mismo resultado.")
    else:
        print("\nLos algoritmos encontraron resultados diferentes.")

        print("\nInversiones con Fuerza Bruta:")
        for inv in resultado_fb["inversiones"]:
            print(f"  Canal: {inv['id_canal']}, Paquete: {inv['id_paquete_seleccionado']}")

        print("\nInversiones con Programación Dinámica:")
        for inv in resultado_pd["inversiones"]:
            print(f"  Canal: {inv['id_canal']}, Paquete: {inv['id_paquete_seleccionado']}")

# Punto de inicio del programa
if __name__ == "__main__":
    comparar_algoritmos()