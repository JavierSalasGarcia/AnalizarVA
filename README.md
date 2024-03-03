# AnalizarVA
Scripts para analizar archivos de Voltametrias a partir de datos de EC-Lab

Instalación:
1) Descargar e instalar Python
2) Ejecutar la terminal de Windows Inicio + "cmd"
3) Instalar las librerias necesarias con:
         pip install scipy chardet matplotlib numpy
5) Ejecución básica del script:
         python AnalizaVA.py
6) Ejecución avanzada del script:
   El script AnalizaVA.py permite el uso de parámetros opcionales -R y -P para modificar el comportamiento del análisis:

Parámetro -R: Permite especificar un valor relacionado con la recomendación de descarte de ciclos basado en criterios específicos de análisis.
Parámetro -P: Define un porcentaje que ajusta ciertos umbrales en el análisis de las curvas, afectando, por ejemplo, la detección de puntos de interés.
Estos parámetros son opcionales y pueden ser combinados de diferentes maneras para ajustar el análisis a las necesidades específicas del usuario. La inclusión de estos parámetros al ejecutar el script modifica los criterios de análisis y la presentación de los resultados, proporcionando flexibilidad en el procesamiento de los datos de voltametría cíclica.

Para utilizar estos parámetros, se añaden al comando de ejecución en la terminal de la siguiente manera: python AnalizaVA.py -R valorR -P valorP, donde valorR y valorP son los valores específicos para cada parámetro
Ejemplo:
          python AnalizaVA.py -R 1 -P 0.1  Añade leyendas que sugieren descartar esa gráfica 

   
