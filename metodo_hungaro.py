# Método húngaro
# Autor: Andrés Gallegos y Santiago Pinto                Fecha: 2024-07-17

INFINITO = float("inf")

PASO_PROCESAR = 1
PASO_REDUCCION_FILAS = 2
PASO_REDUCCION_COLUMNAS = 3
PASO_ASIGNACION_INICIAL = 4
PASO_INICIO_MARCADO = 5
PASO_FIN_MARCADO = 6
PASO_ASIGNACION_FINAL = 7

def hungaro(matriz_costos, minimizar=True, funcion_pasos=None,
            disponibilidad_uniforme=True):
    """Calcula la asignación óptima con el método húngaro.

    La función acepta matrices de costo cuadradas y rectangulares; en el último
    caso, completa las filas o columnas faltantes con ceros.

    'funcion_pasos' es una función que debe tener estos parámetros
    en orden: matriz de costos, matriz de ceros marcados,
    vector de filas marcadas, vector de columnas marcadas,
    asignaciones, código de paso.
    El código de paso corresponde a las constantes PASO_* definidas
    en el módulo.

    PASO_PROCESAR ocurre luego de validar, copiar y procesar la matriz de costos.
        Sólo la matriz de costos no es None
    PASO_REDUCCION_FILAS ocurre luego de restar los menores de cada fila a sus
        filas respectivas.
    PASO_REDUCCION_COLUMNAS ocurre de manera similar que el anterior, pero con
        columnas.
    PASO_ASIGNACION_INICIAL ocurre luego de la búsqueda de la asignación
        inicial, que podría coincidir con la final si satisface las condiciones;
        en este caso, no ocurriría ningún paso siguiente.
        Desde este paso se da el argumento de asignaciones.
    PASO_INICIO_MARCADO ocurre varias veces, antes del subalgoritmo de marcado
        que busca la posibilidad de realizar una reasignación, y luego de
        la primera iteración coincide luego de la ejecución de los pasos
        restantes excepto el final.
        Desde este paso se dan todos los argumentos.
    PASO_FIN_MARCADO ocurre varias veces, luego del marcado y antes de la
        ejecución condicional entre la reasignación y el aligeramiento
        de condiciones óptimas.
    Estos pasos de marcado pueden nunca ocurrir.
    PASO_ASIGNACION_FINAL ocurre luego de obtener la asignación final.

    La función será llamada en cada paso indicado con los argumentos
    correspondientes; dependiendo del paso, algunos pueden ser nulos.
    La función recibe los objetos originales, por lo que no debe modificarlos;
    de lo contrario el programa podría entrar en un estado indefinido.
    Si la función devuelve True a partir de la asignacion inicial, se detiene
    el programa y se devuelve las asignaciones 'tal cual'.
    Si el argumento es None, no se realiza ninguna llamada.
    Se puede utilizar una función predefinida que muestra información
    en la salida estándar pasando True como argumento.

    'disponibilidad_uniforme' indica si todas las filas de la matriz deberían
    tener el mismo tamaño (relevante para una lista de listas).  Si es True
    y la matriz no cumple las restricciones, se genera una excepción.
    Si es False, los datos faltantes se rellenan con infinito positivo.

    Si se produce un error de validación, se lanza una excepción ValueError.
    """
    if funcion_pasos is True:
        funcion_pasos = mostrar_pasos

    validar_matriz(matriz_costos, disponibilidad_uniforme)
    matriz_costos = procesar_matriz(matriz_costos, minimizar,
                                    disponibilidad_uniforme)
    if funcion_pasos is not None:
        argumentos_pasos = [matriz_costos, None, None, None, None]
        funcion_pasos(*argumentos_pasos, PASO_PROCESAR)
    orden = len(matriz_costos)

    for fila in matriz_costos:
        minimo = min(fila)
        for i, costo in enumerate(fila):
            fila[i] = costo - minimo
    if funcion_pasos is not None:
        funcion_pasos(*argumentos_pasos, PASO_REDUCCION_FILAS)

    for j in range(orden):
        minimo = min(matriz_costos[i][j] for i in range(orden))
        for i in range(orden):
            matriz_costos[i][j] = matriz_costos[i][j] - minimo
    if funcion_pasos is not None:
        funcion_pasos(*argumentos_pasos, PASO_REDUCCION_COLUMNAS)

    columnas_marcadas = [False] * orden
    asignaciones = asignar(matriz_costos, columnas_marcadas)
    if funcion_pasos is not None:
        argumentos_pasos[4] = asignaciones
        if funcion_pasos(*argumentos_pasos, PASO_ASIGNACION_INICIAL) == True:
            return asignaciones
    if len(asignaciones) == orden:
        return asignaciones

    filas_marcadas = [False] * orden
    matriz_ceros = [[0] * orden for i in range(orden)]
    for i, j in asignaciones:
        matriz_ceros[i][j] = 1  # Ceros asignados (*)
    falta_reasignar = False
    if funcion_pasos is not None:
        argumentos_pasos[1:4] = [matriz_ceros, filas_marcadas, columnas_marcadas]
    while len(asignaciones) < orden:
        if funcion_pasos is not None:
            if funcion_pasos(*argumentos_pasos, PASO_INICIO_MARCADO) == True:
                return sorted(asignaciones)

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
        if funcion_pasos is not None:
            if funcion_pasos(*argumentos_pasos, PASO_FIN_MARCADO) == True:
                return sorted(asignaciones)

        if falta_reasignar:
            asignaciones = reasignar(matriz_ceros, (i, j), columnas_marcadas)
            filas_marcadas = [False] * orden
            if funcion_pasos is not None:
                argumentos_pasos[2] = filas_marcadas
                argumentos_pasos[4] = asignaciones
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

    asignaciones.sort()
    if funcion_pasos is not None:
        funcion_pasos(*argumentos_pasos, PASO_ASIGNACION_FINAL)
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
                costo = float(costo)
            except (TypeError, ValueError):
                raise ValueError("Los elementos no son números")
            if costo < 0:
                raise ValueError("No puede haber costos negativos")
    if not disponibilidad_uniforme and cant_elementos == 0:
        raise ValueError(ERROR_MATRIZ_VACIA)

def procesar_matriz(matriz_costos, minimizar, disponibilidad_uniforme=True):
    falta_conversion = True
    if isinstance(matriz_costos[0][0], (str, bytes, bytearray)):
        try:
            matriz_costos=[[int(costo) for costo in fila] for fila in matriz_costos]
            falta_conversion = False
        except ValueError:
            pass
    if falta_conversion:
        matriz_costos = \
                  [[float(costo) for costo in fila] for fila in matriz_costos]
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
    if not minimizar:
        maximo = max(map(max, matriz_costos))
        for fila in matriz_costos:
            for j in range(orden):
                fila[j] = maximo - fila[j]
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

def mostrar_pasos(matriz_costos, matriz_ceros, filas_marcadas,
                  columnas_marcadas, asignaciones, paso):
    if paso == PASO_PROCESAR:
        print("Procesada:")
        mostrar_matriz(matriz_costos)
        print()
    elif paso == PASO_REDUCCION_FILAS:
        print("Reducción por filas:")
        mostrar_matriz(matriz_costos)
        print()
    elif paso == PASO_REDUCCION_COLUMNAS:
        print("Reducción por columnas:")
        mostrar_matriz(matriz_costos)
        print()
    elif paso == PASO_ASIGNACION_INICIAL:
        print("Asignación inicial:", asignaciones, end="\n\n")
    elif paso == PASO_INICIO_MARCADO:
        print("Ceros:")
        mostrar_matriz(matriz_ceros)
        print("Costos:")
        mostrar_matriz(matriz_costos)
        print("Filas marcadas:", filas_marcadas)
        print("Columnas marcadas:", columnas_marcadas)
        if input("¿Continuar?: "):
            return True
        print()
    elif paso == PASO_FIN_MARCADO:
        print("Luego de re-marcar:",
              "Ceros:", sep="\n")
        mostrar_matriz(matriz_ceros)
        print("Filas marcadas:", filas_marcadas)
        print("Columnas marcadas:", columnas_marcadas, end="\n\n")
    elif paso == PASO_ASIGNACION_FINAL:
        print("Ceros:")
        mostrar_matriz(matriz_ceros)
        print("Costos:")
        mostrar_matriz(matriz_costos)
        print("Filas marcadas:", filas_marcadas)
        print("Columnas marcadas:", columnas_marcadas)
        print("Asignación final:", asignaciones, end="\n\n")
    else:
        raise NotImplementedError(
            "Paso no implementado en función de muestra integrada")


### Funcion principal para poder ejecutar el programa
def main():
    while True:
        print("+------------------------------------+")
        print("| Método húngaro                     |")
        print("| 1. Ingresar datos y ejecutar       |")
        print("| 2. Salir                           |")
        print("+------------------------------------+\n")
        option = input(">>> Ingrese la opcion que desea: ")
        while option not in ["1", "2"]:
            option = input(">>> Ingrese una opcion valida: ")

        ### Ejecutar el programa
        if option == "1":
            print("\n>>> CARGA DE DATOS...")

            ### Definiendo el tamaño de la matriz
            size = input(">>> Ingrese el tamaño de la matriz: ")
            while size == "" or not size.isdigit():
                size = input(">>> Ingrese un tamaño válido de la matriz: ")

            ### Llenar los datos de la matriz de costos
            print(">>> Ingrese la matriz de costos: ")
            matriz_costos = []

            ### Llenando la matriz de costos
            for i in range(int(size)):
                fila = []
                for j in range(int(size)):
                    costo = input(f">>> Ingrese el costo de la fila {i+1} y columna {j+1}: ")
                    while costo == "" or not costo.isdigit():
                        costo = input(f">>> Ingrese un costo válido de la fila {i+1} y columna {j+1}: ")
                    fila.append(int(costo))
                matriz_costos.append(fila)

            ## Ejecutar el método húngaro
            asignaciones = hungaro(matriz_costos, funcion_pasos=True)
            print("\n>>> Resultado de las asignaciones:\n")
            print(asignaciones)

        ### Salir del programa
        else:
            break

if __name__ == "__main__":
    main()
