import funcionesVA
import pandas as pd
import os
import sys
import argparse

# Obtiene la lista de archivos en la carpeta "pruebas"
files = os.listdir("pruebas")

# Muestra la lista de archivos al usuario y le permite seleccionar uno
print("Archivos que se van a procesar...")
for i, file in enumerate(files):
    print("{}. {}".format(i + 1, file))
    selected = i+1
    # Obtiene el nombre del archivo seleccionado
    filename = files[selected - 1]
    print("procesando el archivo " + filename)

    # Carga el archivo en un DataFrame de pandas
    df = pd.read_csv("pruebas/{}".format(filename), sep='\t', encoding='ISO-8859-1', header=None, skiprows=69)
    df_filtered = df[df[9] == df[9]]

    # Selecciona la columna 10 y conviértela a entero
    col_10 = df_filtered[9].astype(int)

    # Determina el valor máximo de la columna 10
    num_ciclo = col_10.max()

    # Imprime el valor máximo
    print('El número de ciclos de este archivo es: ', num_ciclo)
    print('procesando archivo...')

    # Crear el parser
    parser = argparse.ArgumentParser(description="Este script grafica datos de Voltamperometrias")

    # Agregar argumentos con opciones
    parser.add_argument('-R', '--Recomendacion', type=int, default=0,
                        help='Valor de recomendación. Es opcional y su valor predeterminado es 0.')
    parser.add_argument('-P', '--Porc', type=float, default=0.1,
                        help='Porcentaje. Es opcional y su valor predeterminado es 0.1.')

    # Parsear los argumentos
    args = parser.parse_args()

    # Asignar los argumentos a las variables
    Recomendacion = args.Recomendacion
    Porc = args.Porc

    # Manda llamar a funcionesVA.graficar para procesar cada archivo
    for k2 in range(1, num_ciclo + 1):
        print('Ciclo:', k2)
        funcionesVA.graficar(selected, k2, Recomendacion, Porc)
