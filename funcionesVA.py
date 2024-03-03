import scipy.io
import os
import chardet
import matplotlib.pyplot as plt
import csv
import numpy as np
import scipy.signal

def IntegrarImA(ImA_array, tiempo_array, minimos):
    # Listas para almacenar las integrales de cada intervalo
    integrales_positivas = []
    integrales_negativas = []
    
    # Calcular integrales para cada intervalo definido por los mínimos locales
    for i in range(len(minimos)-1):
        inicio, fin = minimos[i], minimos[i+1]
        ImA_intervalo = ImA_array[inicio:fin]
        tiempo_intervalo = tiempo_array[inicio:fin]
        
        # Integral de la parte positiva
        ImA_positiva = np.where(ImA_intervalo > 0, ImA_intervalo, 0)
        integral_positiva = np.trapz(ImA_positiva, tiempo_intervalo)
        integrales_positivas.append(integral_positiva)
        
        # Integral de la parte negativa
        ImA_negativa = np.where(ImA_intervalo < 0, ImA_intervalo, 0)
        integral_negativa = np.trapz(ImA_negativa, tiempo_intervalo)
        integrales_negativas.append(integral_negativa)
    
    # Calcular el promedio de las integrales positivas y negativas
    prom_integral_positiva= np.mean(integrales_positivas) if integrales_positivas else 0
    prom_integral_negativa = np.mean(integrales_negativas) if integrales_negativas else 0
    return prom_integral_positiva, prom_integral_negativa, minimos

# Función para encontrar los intervalos de integración
def minimos_locales(estimulo):
    # Aplicar un filtro de promedio móvil con una ventana de 200 para suavizar la señal
    def moving_average(signal, window_size=200):
        return np.convolve(signal, np.ones(window_size)/window_size, mode='valid')

    # Suavizar la señal
    estimulo_suavizado = moving_average(estimulo)
    
    # Encontrar los mínimos locales
    minimos = [0]  # Asumimos que el primer punto es un el extremo inicial de integración
    for i in range(1, len(estimulo_suavizado)-1):
        if estimulo_suavizado[i] < estimulo_suavizado[i-1] and estimulo_suavizado[i] < estimulo_suavizado[i+1]:
            minimos.append(i + (200 // 2))  # Ajuste para el índice debido al suavizado
    minimos.append(len(estimulo)-1)  # Asumimos que el último punto es un extremo final de integración
    return minimos

def graficar(selected, num_ciclo, Recomendacion, Porc):
    CicloMal=0
    files = os.listdir("pruebas")
    filename = files[selected - 1]
    # Especifica el número de línea a partir de la cual se deben leer las líneas del archivo
    n = 70
    # Definir el valor de n para el muestreo
    n_muestreo = 7  # Elige el valor deseado para el muestreo
    # Abre el archivo en modo lectura
    with open("pruebas/{}".format(filename), "r", encoding="ISO-8859-1") as f:
        # Lee las líneas del archivo
        lines = f.readlines()
        values = []
        contador_muestreo = 0
        # Itera sobre las líneas
        for line in lines[n:]:
            if contador_muestreo == 0:
                row = line.split("\t")
                # Comprueba si la columna 10 es igual al número de ciclo
                if float(row[9]) == float(num_ciclo):
                    # Itera sobre la lista
                    float_lst = [float(item) for item in row]
                    values.append(float_lst)
            contador_muestreo = (contador_muestreo + 1) % n_muestreo

    # Lee las columnas del archivo de texto con los datos originales y los asigna a las
      # variables del programa. Modificar las columnas si el archivo tiene otra estructura
    tiempo = [row[5] for row in values]
    Ewe = [row[7] for row in values]
    ImA = [row[8] for row in values]
    Ewe_absoluto = [abs(x) for x in Ewe]

    # Encuentra el índice del máximo
    max_ima_index = np.argmax(ImA)

    # Encuentra el máximo de ImA
    max_ima = ImA[max_ima_index]
    min_ima_index = None

    # Recorremos el array buscando el mínimo que cumpla las condiciones
    for i in range(30, len(ImA) - 20):
        if ImA[i] < 0:
            prev_desc_count = sum(1 for j in range(1, 20) if ImA[i-j] > ImA[i])
            next_asc_count = sum(1 for j in range(1, 20) if ImA[i+j] > ImA[i])
            if prev_desc_count >= 40 and next_asc_count >= 40:
                min_ima_index = i
                break

    # Encuentra el índice del mínimo
    min_ima_index = np.argmin(ImA)

    # Si se encontró un mínimo que cumpla las condiciones
    if min_ima_index is not None:
        min_ima = ImA[min_ima_index]
    else:
        print("No se encontró un mínimo que cumpla las condiciones especificadas.")
        min_ima = None

    # Crea una figura con 3 gráficas verticalmente
    fig, ax = plt.subplots(3,1)
    fig.set_size_inches(6, 8)

    fig.subplots_adjust(hspace=0.526)
    # Grafica la columna 8 versus la columna 9 en la primera gráfica
    ax[0].plot(Ewe, ImA)   # Cambiar
    ax[0].set_xlabel("Ewe, V")
    ax[0].set_ylabel("I, mA")

    subcadenas = filename.split("_")
    titulo = subcadenas[0]
    cadena = subcadenas[2]
    subcadenas = cadena.split(".")
    sal = subcadenas[0]
  
    # Dibuja un diamante en el máximo y mínimo
    ax[0].plot(Ewe[max_ima_index], ImA[max_ima_index], marker='D', color='yellow')
    rango_ewe = max(Ewe) - min(Ewe)
    descartada = 0
    if Ewe[min_ima_index] < min(Ewe) + Porc * rango_ewe and Recomendacion == 1:
        ax[0].text(Ewe[min_ima_index], ImA[min_ima_index], "Descartar", fontsize=8, color='red', verticalalignment='bottom')
        descartada = 1

    if min_ima is not None:
        ax[0].plot(Ewe[min_ima_index], ImA[min_ima_index], marker='D', color='black')

    # Grafica Ewe vs tiempo
    ax[1].plot(tiempo, Ewe)
    ax[1].set_xlabel("tiempo, s")
    ax[1].set_ylabel("Ewe, V")

    # 'ImA' y 'tiempo' son listas, convertirlas a arrays de NumPy
    ImA_array = np.array(ImA)
    tiempo_array = np.array(tiempo)
    Ewe_array = np.array(Ewe)

    minimos = minimos_locales(Ewe_array)
    # Calcula la integral de Oxidación (roja) y la de Reducción (azul)
    integral_positiva, integral_negativa, minimos = IntegrarImA(ImA_array, tiempo_array, minimos)
    if len(minimos)>2:
        CicloMal = 1
        prefijo= "m" + str(len(minimos)-1) + "_"
    else:
        prefijo= ""


    Integrales_oxid = integral_positiva
    Integrales_oxid_redondeada = round(Integrales_oxid,1)

    # Integral de los semiciclos negativos (reducción) 
    Integrales_redu = integral_negativa
    Integrales_redu_redondeada = round(Integrales_redu, 1)
    # Imprimir las integrales
    print("Integral de la parte positiva (roja):", integral_positiva)
    print("Integral de la parte negativa (azul):", integral_negativa)

    # Grafica Ima vs tiempo en dos colores. Rojo positivos, azul negativos
    ax[2].fill_between(tiempo, ImA, 0, where=[x > 0 for x in ImA], color='red')
    ax[2].fill_between(tiempo, ImA, 0, where=[x < 0 for x in ImA], color='blue')
    ax[2].set_xlabel("tiempo, s")
    ax[2].set_ylabel("I, mA")

    # Dibuja un diamante en el máximo y mínimo
    ax[2].plot(tiempo[max_ima_index], max_ima, marker='D', color='yellow')
    if min_ima is not None:
        ax[2].plot(tiempo[min_ima_index], min_ima, marker='D', color='black')

    ax[2].set_xlabel("tiempo, s")
    ax[2].set_ylabel("I, mA")

    parts = filename.split('_')

    # Elimina las partes de texto que no necesitas
    del parts[1:2]  # Esto elimina los elementos en las posiciones 1 y 2

    # Vuelve a unir las partes restantes
    cleaned_filename = '_'.join(parts)

    # Reemplaza "txt" por una cadena vacía
    cleaned_filename = cleaned_filename.replace('.txt', '')

    # Añade el número de ciclo al final
    tituloGrafica = cleaned_filename + " Ciclo:" + str(num_ciclo)

   
    # Obtén los límites actuales del eje y
    y_min, y_max = ax[2].get_ylim()

    # Calcula una posición para la leyenda ligeramente por debajo del límite superior
    y_pos_leyenda = y_max - (y_max - y_min) * 0.05  # Ajusta el 0.05 si es necesario
    # Coloca la leyenda en la posición calculada
    ax[2].text(tiempo[i], y_pos_leyenda, Integrales_oxid_redondeada, fontsize=6, color='red', verticalalignment='top')

    # Calcula una posición para la leyenda ligeramente por encima del límite inferior
    y_pos_leyenda = y_min + (y_max - y_min) * 0.05  # Ajusta el 0.05 si es necesario
    # Coloca la leyenda en la posición calculada
    ax[2].text(tiempo[i], y_pos_leyenda, Integrales_redu_redondeada, fontsize=6, color='blue', verticalalignment='bottom')


    with open("pruebas/{}".format(filename), "r", encoding="ISO-8859-1") as f:
        # Lee todas las líneas del archivo
        lines = f.readlines()

    # Guarda la figura como imagen en formato JPG
     # Reemplaza "txt" por una cadena vacía
    cleaned_filename2 = filename.replace('.txt', '')
    if not os.path.exists("graficas"):
        os.makedirs("graficas")
    if descartada == 0:
        fig.savefig("graficas/" + prefijo + cleaned_filename2 + "_" + str(num_ciclo) +".jpg", dpi=300)
    else:
        fig.savefig("graficas/x" + prefijo + cleaned_filename2 + "_" + str(num_ciclo) +".jpg", dpi=300)
    plt.close(fig)

    # Generar el nombre del archivo con el número de ciclo
    if descartada == 0:
        nombre_archivo = "DatosCiclo/{}{}_ciclo{}.txt".format(prefijo,filename, num_ciclo)
    else:
        nombre_archivo = "DatosCiclo/x{}{}_ciclo{}.txt".format(prefijo, filename, num_ciclo)

    if not os.path.exists("DatosCiclo"):
        os.makedirs("DatosCiclo")

    with open(nombre_archivo, "w") as f:
        for tiempo_val, ewe_val, ima_val in zip(tiempo, Ewe, ImA):
            f.write("{},{}, {}\n".format(tiempo_val, ewe_val, ima_val))
    Ewe[max_ima_index], ImA[max_ima_index]
        
    # Si min_ima_index es None, asigna "NaN" a Ewe y ImA. En caso contrario, usa los valores indexados
    Ewe_min_ima = "NaN" if min_ima_index is None else Ewe[min_ima_index]
    ImA_min_ima = "NaN" if min_ima_index is None else ImA[min_ima_index]

    linea = [filename, str(num_ciclo), Integrales_oxid_redondeada, Integrales_redu_redondeada, Ewe[max_ima_index],ImA[max_ima_index], Ewe_min_ima, ImA_min_ima]

    nombre_archivo_cargas = "cargas.csv"
    # Abre el archivo para leer y escribir. Si no existe, lo crea.
    with open(nombre_archivo_cargas, "a+", newline="") as archivo:
        # Mueve el cursor al inicio del archivo para verificar si está vacío
        archivo.seek(0)
        # Verifica si el archivo está vacío leyendo el primer caracter
        primer_caracter = archivo.read(1)
        # Si el archivo está vacío, no habrá ningún caracter leído
        if not primer_caracter:
            archivo.write("Prueba, ciclo, Qo, Qr, Epa, Ipa, Epc, Ipc\n")
        # Si necesitas agregar más datos después, asegúrate de mover el cursor al final del archivo
        archivo.seek(0, os.SEEK_END)
    with open("cargas.csv", mode="a", newline="") as archivo:
        escritor_csv = csv.writer(archivo, delimiter=",")
        escritor_csv.writerow(linea)