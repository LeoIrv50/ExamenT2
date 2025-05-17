def optimizar_gasto_programacion_dinamica(canales_publicitarios, presupuesto_total, reglas_sinergia):
    """
    Esta función busca optimizar el gasto en publicidad para maximizar el retorno,
    teniendo en cuenta posibles sinergias entre canales.
    """

    # 1️⃣ Guardamos todos los paquetes disponibles en un diccionario para accederlos fácilmente
    paquetes_por_id = {}
    for canal in canales_publicitarios:
        id_canal = canal["id_canal"]
        for paquete in canal["paquetes_disponibles"]:
            paquetes_por_id[(id_canal, paquete["id_paquete"])] = paquete

    # 2️⃣ Función para calcular el costo total de una selección de paquetes
    def calcular_costo(seleccion):
        total = 0
        for canal_id, id_paquete in seleccion.items():
            if id_paquete is not None:
                total += paquetes_por_id[(canal_id, id_paquete)]["costo_paquete"]
        return total

    # 3️⃣ Función para calcular el retorno considerando las sinergias activas
    def calcular_retorno_con_sinergias(seleccion):
        # Inicializamos los multiplicadores de cada canal a 1.0
        multiplicadores = {canal["id_canal"]: 1.0 for canal in canales_publicitarios}

        # Verificamos cada regla de sinergia
        for regla in reglas_sinergia:
            id_activador = regla["canal_activador_id"]
            id_beneficiado = regla["canal_beneficiado_id"]
            paquete_minimo = regla["paquete_activador_min_id"]

            # Verificamos si el canal activador tiene un paquete seleccionado
            if id_activador in seleccion and seleccion[id_activador] is not None:
                # Obtenemos los paquetes relevantes
                paquete_seleccionado = seleccion[id_activador]

                # Verificamos si el paquete cumple con el requisito mínimo
                if id_beneficiado in seleccion and seleccion[id_beneficiado] is not None:
                    paquete_activador = paquetes_por_id.get((id_activador, paquete_seleccionado))
                    paquete_min = paquetes_por_id.get((id_activador, paquete_minimo))

                    if paquete_activador["costo_paquete"] >= paquete_min["costo_paquete"]:
                        # Aplicamos el multiplicador al canal beneficiado
                        multiplicadores[id_beneficiado] *= regla["factor_multiplicador_retorno"]

        # Calculamos el retorno total aplicando los multiplicadores
        retorno_total = 0
        detalle_retornos = {}

        for canal_id, id_paquete in seleccion.items():
            if id_paquete is not None:
                paquete = paquetes_por_id[(canal_id, id_paquete)]
                retorno_base = paquete["retorno_esperado_base"]
                retorno_final = retorno_base * multiplicadores[canal_id]

                detalle_retornos[canal_id] = {
                    'retorno_base': retorno_base,
                    'multiplicador': multiplicadores[canal_id],
                    'retorno_final': retorno_final
                }
                retorno_total += retorno_final

        return retorno_total, detalle_retornos

    # 4️⃣ Programación dinámica con memoización
    memo = {}

    def dp(indice_canal, presupuesto_restante, seleccion_actual):
        if indice_canal == len(canales_publicitarios):
            retorno, detalles = calcular_retorno_con_sinergias(seleccion_actual)
            return retorno, seleccion_actual, detalles

        # Clave para memoización
        clave_memo = (indice_canal, presupuesto_restante, tuple(sorted(seleccion_actual.items())))
        if clave_memo in memo:
            return memo[clave_memo]

        # Canal actual que estamos procesando
        canal_actual = canales_publicitarios[indice_canal]
        id_canal = canal_actual["id_canal"]

        # Opción 1: No seleccionar ningún paquete para este canal
        seleccion_actual_copia = seleccion_actual.copy()
        retorno_no_elegido, mejores_selecciones, mejores_detalles = dp(indice_canal + 1,
                                                                       presupuesto_restante,
                                                                       seleccion_actual_copia)

        mejor_retorno = retorno_no_elegido
        mejor_seleccion = mejores_selecciones
        mejores_detalles_retorno = mejores_detalles

        # Opción 2: Probar cada paquete disponible para este canal
        for paquete in canal_actual["paquetes_disponibles"]:
            costo_paquete = paquete["costo_paquete"]
            id_paquete = paquete["id_paquete"]

            # Verificar que haya presupuesto suficiente
            if costo_paquete <= presupuesto_restante:
                seleccion_paquete = seleccion_actual.copy()
                seleccion_paquete[id_canal] = id_paquete

                retorno_con_paquete, seleccion_con_paquete, detalles_con_paquete = dp(indice_canal + 1,
                                                                                      presupuesto_restante - costo_paquete,
                                                                                      seleccion_paquete)

                if retorno_con_paquete > mejor_retorno:
                    mejor_retorno = retorno_con_paquete
                    mejor_seleccion = seleccion_con_paquete
                    mejores_detalles_retorno = detalles_con_paquete

        # Guardar en memo para evitar recálculos
        memo[clave_memo] = (mejor_retorno, mejor_seleccion, mejores_detalles_retorno)
        return mejor_retorno, mejor_seleccion, mejores_detalles_retorno

    # 5️⃣ Ejecutar algoritmo
    retorno_optimo, seleccion_optima, detalles_retorno = dp(0, presupuesto_total, {})

    # 6️⃣ Generar resultado final
    inversiones = []
    for canal_id, id_paquete in seleccion_optima.items():
        if id_paquete is not None:
            paquete = paquetes_por_id[(canal_id, id_paquete)]

            # Obtener el retorno final después de aplicar sinergias
            retorno_final = detalles_retorno[canal_id]['retorno_final'] if canal_id in detalles_retorno else paquete[
                "retorno_esperado_base"]

            inversiones.append({
                "id_canal": canal_id,
                "id_paquete_seleccionado": id_paquete,
                "costo_del_paquete_seleccionado": paquete["costo_paquete"],
                "retorno_final_del_canal": retorno_final
            })

    # Calcular totales
    costo_total = sum(inv["costo_del_paquete_seleccionado"] for inv in inversiones)
    retorno_total = sum(inv["retorno_final_del_canal"] for inv in inversiones)

    resumen_global = {
        "costo_total_invertido_calculado": costo_total,
        "retorno_total_final_esperado_calculado": retorno_total,
        "presupuesto_restante": presupuesto_total - costo_total
    }

    return {
        "inversiones": inversiones,
        "resumen_global": resumen_global
    }