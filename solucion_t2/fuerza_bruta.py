from itertools import product

def optimizar_gasto(canales, presupuesto_total, reglas_sinergia):
    # Generar todas las combinaciones posibles de paquetes por canal
    combinaciones = []
    for canal in canales:
        opciones = []

        # Agregar opción de no invertir en este canal
        opciones.append(None)

        # Agregar cada paquete disponible como opción
        for paquete in canal["paquetes_disponibles"]:
            opciones.append((canal["id_canal"], paquete))

        combinaciones.append(opciones)

    # Generar todas las combinaciones posibles (producto cartesiano)
    todas_las_combinaciones = list(product(*combinaciones))
    # Preparar diccionario para buscar paquetes por (canal_id, paquete_id)
    todos_paquetes = {}
    for canal in canales:
        for paquete in canal["paquetes_disponibles"]:
            clave = (canal["id_canal"], paquete["id_paquete"])
            todos_paquetes[clave] = paquete

    mejor_retorno = 0
    mejor_inversion = None
    mejor_detalle = None

    # Evaluar cada combinación
    for combinacion in todas_las_combinaciones:
        paquetes_seleccionados = [p for p in combinacion if p is not None]

        # Calcular costo total de esta combinación
        costo_total = 0
        for canal_id, paquete in paquetes_seleccionados:
            costo_total += paquete["costo_paquete"]

        if costo_total > presupuesto_total:
            continue  # Saltar si excede el presupuesto

        # Calcular retorno con sinergias
        retorno_total, detalle = calcular_retorno(paquetes_seleccionados, reglas_sinergia, todos_paquetes)

        # Actualizar mejor solución
        if retorno_total > mejor_retorno:
            mejor_retorno = retorno_total
            mejor_inversion = paquetes_seleccionados
            mejor_detalle = detalle

    # Si encontramos una buena combinación
    if mejor_inversion:
        resultado = {"inversiones": [], "resumen_global": {}}

        # Llenar inversiones
        for canal_id, paquete in mejor_inversion:
            resultado["inversiones"].append({
                "id_canal": canal_id,
                "id_paquete_seleccionado": paquete["id_paquete"],
                "costo_del_paquete_seleccionado": paquete["costo_paquete"],
                "retorno_final_del_canal": mejor_detalle[canal_id]
            })

        # Llenar resumen global
        costo_total = sum(p["costo_paquete"] for _, p in mejor_inversion)
        retorno_total = sum(mejor_detalle.values())

        resultado["resumen_global"] = {
            "costo_total_invertido_calculado": costo_total,
            "retorno_total_final_esperado_calculado": retorno_total,
            "presupuesto_restante": presupuesto_total - costo_total
        }

        return resultado

    return None  # No se encontró ninguna combinación válida


def calcular_retorno(seleccionados, reglas_sinergia, todos_paquetes):
    # Guardar retorno base y multiplicador por canal
    paquetes_por_canal = {canal_id: paquete for canal_id, paquete in seleccionados}
    multiplicadores = {canal_id: 1.0 for canal_id, _ in seleccionados}

    # Aplicar las reglas de sinergia
    for regla in reglas_sinergia:
        canal_activador = regla["canal_activador_id"]
        id_paquete_min = regla["paquete_activador_min_id"]
        canal_beneficiado = regla["canal_beneficiado_id"]
        factor = regla["factor_multiplicador_retorno"]

        # Verificar si el canal activador está seleccionado
        if canal_activador in paquetes_por_canal:
            paquete_activador = paquetes_por_canal[canal_activador]
            paquete_min = todos_paquetes.get((canal_activador, id_paquete_min))

            if paquete_min and paquete_activador["costo_paquete"] >= paquete_min["costo_paquete"]:
                # Aplicar sinergia si el canal beneficiado también fue seleccionado
                if canal_beneficiado in multiplicadores:
                    multiplicadores[canal_beneficiado] *= factor

    # Calcular retornos finales
    detalles = {}
    for canal_id, paquete in paquetes_por_canal.items():
        retorno_base = paquete["retorno_esperado_base"]
        detalles[canal_id] = retorno_base * multiplicadores[canal_id]

    retorno_total = sum(detalles.values())
    return retorno_total, detalles