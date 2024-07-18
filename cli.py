#!/usr/bin/env python3
# Interfaz interactiva de consola para resolver problemas de
# transporte y asignación
# Autor: Andrés Gallegos y Santiago Pinto               Fecha: 2024-07-18

import sys
import metodo_hungaro as mh

funcion_estado = None

def main():
    global funcion_estado
    funcion_estado = inicio
    try:
        while funcion_estado is not None:
            funcion_estado()
    except KeyboardInterrupt:
        print("...terminación forzada...", file=sys.stderr)
    print("\nPrograma terminado.")

def inicio():
    global funcion_estado
    print("",
          "(t) Resolver problemas de transporte",
          "(a) Resolver problemas de asignación",
          "(0) Salir del programa",
          sep="\n")
    opcion = input("Indique la opción deseada con una letra: ").strip()

    if opcion == "t":
        funcion_estado = transporte
    elif opcion == "a":
        funcion_estado = asignacion
    elif opcion == "0":
        funcion_estado = None
    else:
        print("Opción incorrecta.", file=sys.stderr)

def transporte():
    global funcion_estado
    print("Función no disponible.", file=sys.stderr)
    funcion_estado = inicio

def asignacion():
    global funcion_estado
    matriz_costos = []
    entrada = " "
    print("Introduzca a continuación los elementos de la matriz de costos,"
          " fila por fila, separando elementos con espacios, e indicando"
          " el fin de los datos con una fila vacía.")
    try:
        while True:
            entrada = input("Fila: ").replace(",", ".")
            if entrada == "":
                break
            matriz_costos.append(entrada.split())
    except:
        print("Hay problemas con los datos introducidos.  Intente nuevamente.",
              file=sys.stderr)
        funcion_estado = inicio
        return

    if len(matriz_costos) == 0:
        print("No se introdujeron datos.", file=sys.stderr)
        funcion_estado = inicio
        return

    matriz_costos = [list(map(float, fila)) for fila in matriz_costos]
    try:
        asignaciones = mh.hungaro(matriz_costos, minimizar, funcion_pasos=True)
    except ValueError as e:
        print("Los datos introducidos son inválidos:",
              "\t" + e.args[0],
              sep="\n", file=sys.stderr)
        funcion_estado = inicio
        return

    matriz_costos = mh.procesar_matriz(matriz_costos, True)
    salida = [["Centro", "Ruta", "Costo"]]
    salida += ([str(par[0] + 1), str(par[1] + 1),
                str(matriz_costos[par[0]][par[1]]) ]
               for par in asignaciones )
    salida += [["Total", "",
                str(sum(matriz_costos[i][j] for i, j in asignaciones)) ]]
    mostrar_tabla(salida)

    funcion_estado = inicio

def mostrar_tabla(tabla):
    if len(tabla) == 0:
        return

    anchos = [0] * len(tabla[0])
    for fila in tabla:
        for j in range(len(fila)):
            anchos[j] = max(len(fila[j]), anchos[j])
    #plantillas = ["{:^%d}" % ancho for ancho in anchos]
    linea_horizontal = "|" + "-" * (sum(anchos) + len(anchos) - 1) + "|"
    iterador_tabla = iter(tabla)

    print("+", linea_horizontal[1:-1], "+", sep="")
    print("|", end="")
    print(*(campo.center(ancho)
            for ancho, campo in zip(anchos, next(iterador_tabla)) ),
          sep="|", end="")
    print("|")
    for fila in iterador_tabla:
        print(linea_horizontal)
        print("|", end="")
        print(*(campo.center(ancho)
                for ancho, campo in zip(anchos, fila)),
              sep="|", end="")
        print("|")
    print("+", linea_horizontal[1:-1], "+", sep="", end="\n\n")

if __name__ == "__main__":
    main()
