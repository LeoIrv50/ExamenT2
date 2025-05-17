canales_publicitarios = [
   {
      "id_canal":"RedesSociales",
      "paquetes_disponibles":[
         {
            "id_paquete":"RS_Basico",
            "costo_paquete":100,
            "retorno_esperado_base":500
         },
         {
            "id_paquete":"RS_Medio",
            "costo_paquete":200,
            "retorno_esperado_base":900
         },
         {
            "id_paquete":"RS_Alto",
            "costo_paquete":300,
            "retorno_esperado_base":1200
         }
      ]
   },
   {
      "id_canal":"BusquedaAds",
      "paquetes_disponibles":[
         {
            "id_paquete":"Busq_Basico",
            "costo_paquete":150,
            "retorno_esperado_base":600
         },
         {
            "id_paquete":"Busq_Medio",
            "costo_paquete":250,
            "retorno_esperado_base":950
         }
      ]
   },
   {
      "id_canal":"VideoPremium",
      "paquetes_disponibles":[
         {
            "id_paquete":"VidP_Unico",
            "costo_paquete":400,
            "retorno_esperado_base":1500
         }
      ]
   }
]


reglas_sinergia = [
   {
      "id_regla":"Sinergia_RS_Busqueda",
      "canal_activador_id":"RedesSociales",
      "paquete_activador_min_id":"RS_Medio",
      "canal_beneficiado_id":"BusquedaAds",
      "factor_multiplicador_retorno":1.25
   },
   {
      "id_regla":"Sinergia_Video_General",
      "canal_activador_id":"VideoPremium",
      "paquete_activador_min_id":"VidP_Unico",
      "canal_beneficiado_id":"RedesSociales",
      "factor_multiplicador_retorno":1.10
   }
]

presupuesto_total_campana = 700