import numpy as np
import pandas as np
from pulp import *
from pandas import DataFrame

def costo_transporte_ruta_minima(oferta, demanda, origen, destino, costo_envio):
  ### Declaramos la función objetivo... nota que buscamos minimizar el costo(LpMinimize)
  prob = LpProblem('Transporte', LpMinimize)

  rutas = [(i,j) for i in origen for j in destino]
  cantidad = LpVariable.dicts('Cantidad de Envio',(origen,destino),0)
  prob += lpSum(cantidad[i][j]*costo_envio[i][j] for (i,j) in rutas)
  for j in destino:
      prob += lpSum(cantidad[i][j] for i in origen) == demanda[j]
  for i in origen:
      prob += lpSum(cantidad[i][j] for j in destino) <= oferta[i]
  ### Resolvemos e imprimimos el Status, si es Optimo, el problema tiene solución.
  prob.solve()
  print("Status:", LpStatus[prob.status])

  ### Imprimimos la solución
  for v in prob.variables():
      if v.varValue > 0:
          print(v.name, "=", v.varValue)
  print('El costo mínimo es:', value(prob.objective))

def main():
  while True:
    print("+------------------------------------+")
    print("| Método de transporte Vogel         |")
    print("| 1. Ingresar datos y ejecutar       |")
    print("| 2. Salir                           |")
    print("+------------------------------------+\n")

    ### Opcion del usuario
    option = input(">>> Ingrese la opcion que desea: ")
    while option not in ["1", "2"]:
      option = input(">>> Ingrese una opcion valida: ") 
    
    # Ejecutar el algoritmo
    if option == "1":
      print(">>> Ejecutando el método de transporte Vogel...")

      # ALMACENES Y OFERTAS
      cantidad_origenes = input(">>> Ingrese la cantidad de almacenes: ")
      ### Validar que sea un digito
      while cantidad_origenes == "" or not cantidad_origenes.isdigit():
        cantidad_origenes = input(">>> Ingrese una cantidad válida de almacenes: ")
      # Almacenes y sus ofertas 
      origen = [] # Array con el nombre de los origenes
      ofertas = [] # Array con las ofertas de los origenes
      oferta = {} # Diccionario con el nombre del almacen y su oferta
      for i in range(int(cantidad_origenes)):
        almacen = input("\n>>> Ingrese el nombre del almacen: ")
        oferta_almacen = input(">>> Ingrese la oferta del almacen: ")
        ## Validar que sea un digito
        while oferta_almacen == "" or not oferta_almacen.isdigit():
          oferta_almacen = input(">>> Ingrese una oferta válida del almacen {almacen}: ")
        ### Almacenando los valores obtenidos
        origen.append(almacen) # Array con los nombres de los origenes
        ofertas.append(int(oferta_almacen)) # Array con las ofertas de los origenes
        oferta[almacen] = int(oferta_almacen) # Diccionario clave(nombre del almacen)-valor(oferta


      # DISTRIBUIDORES Y DEMANDA
      cantidad_destinos = input("\n>>> Ingrese la cantidad de centros de distribución: ")
      ### Validar que sea un digito
      while cantidad_destinos == "" or not cantidad_destinos.isdigit():
        cantidad_destinos = input(">>> Ingrese una cantidad válida de centros de distribución: ")
      # Distribuidores y demanda
      destino = [] # Array con el nombre de los destinos
      destinos = [] # Array con las demandas de los destinos
      demanda = {} # Diccionario con el nombre del centro de distribución y su demanda
      for i in range(int(cantidad_destinos)):
        distribuidor = input("\n>>> Ingrese el nombre del centro de distribución: ")
        demanda_distribuidor = input(f">>> Ingrese la demanda del centro de distribución {distribuidor}: ")
        ## Validar que sea un digito
        while demanda_distribuidor == "" or not demanda_distribuidor.isdigit():
          demanda_distribuidor = input(">>> Ingrese una demanda válida del centro de distribución: ")
        ### Almacenando los valores obtenidos
        destino.append(distribuidor)
        destinos.append(int(demanda_distribuidor))
        demanda[distribuidor] = int(demanda_distribuidor)

      # Costo de transporte
      print("\n>>> Costos de transporte de cada almacén a cada centro de distribución")
      costos_transporte = {}
      costo_fila = {}
      for i in origen:
        for j in destino:
          costo = input(f">>> Ingrese el costo de transporte de {i} a {j}: ")
          ## Validar que sea un digito
          while costo == "" or not costo.isdigit():
            costo = input(f">>> Ingrese un costo válido de transporte de {i} a {j}: ")
          costo_fila[j] = int(costo)
        costos_transporte[i] = costo_fila
      
      # Calcular los resultados
      costo_transporte_ruta_minima(oferta, demanda, origen, destino, costos_transporte)
      
    # Salir del programa
    else:
      break

if __name__ == "__main__":
  main()
