# Método húngaro
# Autor: Santiago Pinto             Fecha: 2024-07-13

INFINITO = float("inf")

def hungaro(matriz_costos, disponibilidad_uniforme=True):
    validar_matriz(matriz_costos, disponibilidad_uniforme)
    matriz_costos = procesar_matriz(matriz_costos, disponibilidad_uniforme)
    print("Procesada:")
    mostrar_matriz(matriz_costos)
    print()
    orden = len(matriz_costos)
    
    for fila in matriz_costos:
        minimo = min(fila)
        for i, costo in enumerate(fila):
            fila[i] = costo - minimo
    print("Reducción por filas:")
    mostrar_matriz(matriz_costos)
    print()
    for j in range(orden):
        minimo = min(matriz_costos[i][j] for i in range(orden))
        for i in range(orden):
            matriz_costos[i][j] = matriz_costos[i][j] - minimo
    print("Reducción por columnas:")
    mostrar_matriz(matriz_costos)
    print()

    columnas_marcadas = [False] * orden
    asignaciones = asignar(matriz_costos, columnas_marcadas)
    if len(asignaciones) == orden:
        return asignaciones
    print("Asignación inicial:", asignaciones, end="\n\n")

    filas_marcadas = [False] * orden
    matriz_ceros = [[0] * orden for i in range(orden)]
    for i, j in asignaciones:
        matriz_ceros[i][j] = 1  # Ceros asignados (*)
    falta_reasignar = False
    while len(asignaciones) < orden:
        print("Ceros:")
        mostrar_matriz(matriz_ceros)
        print("Costos:")
        mostrar_matriz(matriz_costos)
        print("Filas marcadas:", filas_marcadas)
        print("Columnas marcadas:", columnas_marcadas)
        if input("¿Continuar?: "):
            return sorted(asignaciones)
        print()
        
        minimo = INFINITO
        for i in range(orden):
            if filas_marcadas[i]:
                continue
            fila = matriz_costos[i]
            minimo_fila = INFINITO
            quedan_ceros = False
            for j in range(orden):
                if not columnas_marcadas[j]:
                    costo = fila[j]
                    if costo == 0:
                        quedan_ceros = True
                        break
                    elif costo < minimo_fila:
                        minimo_fila = costo
            if not quedan_ceros:
                if minimo_fila < minimo:
                    minimo = minimo_fila
                continue
            matriz_ceros[i][j] = 2  # Ceros candidatos (')
            try:
                j = matriz_ceros[i].index(1)
            except ValueError:
                falta_reasignar = True
                break
            filas_marcadas[i] = True
            columnas_marcadas[j] = False
        print("Luego de re-marcar:",
              "Ceros:", sep="\n")
        mostrar_matriz(matriz_ceros)
        print("Filas marcadas:", filas_marcadas)
        print("Columnas marcadas:", columnas_marcadas, end="\n\n")

        if falta_reasignar:
            asignaciones = reasignar(matriz_ceros, (i, j), columnas_marcadas)
            filas_marcadas = [False] * orden
            falta_reasignar = False
            continue
        for i, fila in enumerate(matriz_costos):
            if filas_marcadas[i]:
                for j in range(orden):
                    if columnas_marcadas[j]:
                        fila[j] += minimo
            else:
                for j in range(orden):
                    if not columnas_marcadas[j]:
                        fila[j] -= minimo

    print("Ceros:")
    mostrar_matriz(matriz_ceros)
    print("Costos:")
    mostrar_matriz(matriz_costos)
    print("Filas marcadas:", filas_marcadas)
    print("Columnas marcadas:", columnas_marcadas)
    print("Asignación final:", asignaciones, end="\n\n")

    asignaciones.sort()
    return asignaciones

def validar_matriz(matriz_costos, disponibilidad_uniforme=True):
    ERROR_MATRIZ_VACIA = "La matriz está vacía"
    if len(matriz_costos) == 0:
        raise ValueError(ERROR_MATRIZ_VACIA)
    cant_elementos = 0
    largo_fila = len(matriz_costos[0])
    if disponibilidad_uniforme and largo_fila == 0:
        raise ValueError(ERROR_MATRIZ_VACIA)
    for fila in matriz_costos:
        if disponibilidad_uniforme:
            if len(fila) != largo_fila:
                raise ValueError("Las filas no tienen el mismo tamaño")
        else:
            cant_elementos += len(fila)
        for costo in fila:
            try:
                float(costo)
            except (TypeError, ValueError):
                raise ValueError("Los elementos no son números")
            if costo < 0:
                raise ValueError("No puede haber costos negativos")
    if not disponibilidad_uniforme and cant_elementos == 0:
        raise ValueError(ERROR_MATRIZ_VACIA)

def procesar_matriz(matriz_costos, disponibilidad_uniforme=True):
    matriz_costos = [[float(costo) for costo in fila] for fila in matriz_costos]
    cant_filas = len(matriz_costos)
    if disponibilidad_uniforme:
        orden = max(cant_filas, len(matriz_costos[0]))
    else:
        orden = max(cant_filas, *map(len, matriz_costos))
    if cant_filas == orden:
        if disponibilidad_uniforme:
            faltante = orden - len(matriz_costos[0])
            if faltante > 0:
                for fila in matriz_costos:
                    fila.extend([0] * faltante)
        else:
            largo_fila_max = max(map(len, matriz_costos))
            faltante = orden - largo_fila_max
            for fila in matriz_costos:
                largo_fila = len(fila)
                if largo_fila < largo_fila_max:
                    fila.extend([INFINITO] * (largo_fila_max - largo_fila))
                if faltante > 0:
                    fila.extend([0] * faltante)
    else:
        matriz_costos.extend([[0] * orden for i in range(orden - cant_filas)])
    return matriz_costos

def asignar(matriz_costos, columnas_excluidas=None):
    ceros_por_fila = [fila.count(0) for fila in matriz_costos]
    asignaciones = []
    orden = len(matriz_costos)
    if columnas_excluidas is None:
        columnas_excluidas = [False] * orden

    while len(asignaciones) < orden:
        try:
            i = obtener_siguiente_asignacion(ceros_por_fila)
        except ValueError as e:  # Hay error si y solo si no quedan ceros
            asignaciones.sort()
            return asignaciones
        fila = matriz_costos[i]
        #quedan_ceros = False
        for j, costo in enumerate(fila):
            if costo == 0 and not columnas_excluidas[j]:
                #quedan_ceros = True
                break
        #if not quedan_ceros:
        #    asignaciones.sort()
        #    return asignaciones
        columnas_excluidas[j] = True
        ceros_por_fila[i] = 0  # Esto implica [1]
        for k, fila in enumerate(matriz_costos):
            if k != i and fila[j] == 0:  #<- Se puede evitar [1] con un extra
                ceros_por_fila[k] -= 1  # [1] que la cuenta puede dar negativa
        asignaciones.append((i, j))

    asignaciones.sort()
    return asignaciones

def obtener_siguiente_asignacion(ceros_por_fila):
    indice_fila = min((cuenta, i) for i, cuenta in enumerate(ceros_por_fila)
                                  if cuenta > 0)[1]
    return indice_fila

##def obtener_asignaciones_faltantes(ceros_por_fila):
##    filas_por_asignar = [(cuenta, i) for i, cuenta in enumerate(ceros_por_fila)
##                                     if cuenta > 0]
##    filas_por_asignar.sort(reverse=True)
##    return filas_por_asignar

def reasignar(matriz_ceros, posicion_cero, columnas_marcadas):
    orden = len(matriz_ceros)
    #camino = [posicion_cero]
    i_previo, j = posicion_cero
    hay_asignado = True
    while hay_asignado:
        hay_asignado = False
        for i in range(orden):
            fila = matriz_ceros[i]
            if fila[j] == 1:
                matriz_ceros[i_previo][j] = 1
                matriz_ceros[i][j] = 0
                #camino.append((i, j))
                j = fila.index(2)
                #camino.append((i, j))
                i_previo = i
                hay_asignado = True
                break
    matriz_ceros[i_previo][j] = 1

    for i in range(orden):
        columnas_marcadas[i] = False
    asignaciones = []
    for i, fila in enumerate(matriz_ceros):
        for j, marca in enumerate(fila):
            if marca == 1:
                columnas_marcadas[j] = True
                asignaciones.append((i, j))
            elif marca == 2:
                fila[j] = 0
    return asignaciones

def mostrar_matriz(matriz):
    for fila in matriz:
        print("[", *("%5d" % elemento for elemento in fila), "]")
