import pandas as pd
import numpy as np
import csv
import re
import matplotlib.pyplot as plt

#creamos lista para añadirle los valores de magnitud absoluta
List = []

#creamos una lista para añadirle los nombres de las estrellas
nombre_propio_list = []

#convertimos de string a float arreglando el problema del menos raro
def convert_to_float(value):
    value = value.replace(',', '.')  #sustituimos las comas por puntos
    return float(re.sub('[^0-9eE.+-]', '', value.replace('−', '-')))

try:
    #abrimos el csv
    with open('Tabla.csv', 'r', encoding='utf-8') as file:
        #leemos el contenido
        csv_reader = csv.reader(file)
        header = next(csv_reader)  #conseguimos el header

        #Sacamos el i de la columna d nombre propio, es indiferente que sea mayuscula o minuscula
        nombre_propio_index = next((i for i, col in enumerate(header) if col.strip().lower() == 'nombre propio'), None)

        if nombre_propio_index is None:
            raise ValueError("Column 'Nombre Propio' not found in the CSV header.")

        for row in csv_reader:
            #saltarse las filas con distinto número de columnas
            if len(row) != len(header):
                continue

            #pintamos cada fila
            print(row)

            #accedemos a cada fila por su i
            magnitud_aparente = convert_to_float(row[1])
            distancia_años_luz = convert_to_float(row[4])

            #calcular magnitud absoluta y añadirla a la lista
            distancia_parsecs = distancia_años_luz / 3.2616
            magnitud_absoluta = magnitud_aparente - 5 * (np.log10(distancia_parsecs) - 1)
            List.append(magnitud_absoluta)

            #añadir nombre propio a la lista
            nombre_propio_value = row[nombre_propio_index]
            nombre_propio_list.append(nombre_propio_value)

except FileNotFoundError:
    print("The specified CSV file was not found.")

except Exception as e:
    print(f"An error occurred: {e}")

#creamos nuevo dataframe solo con los datos que nos interesan
df = pd.DataFrame({'Nombre Propio': nombre_propio_list, 'Magnitud Absoluta': List})

#creamos otra columna para la luminosidad
df['Luminosidad'] = 10 ** ((4.83 - df['Magnitud Absoluta']) / 2.5)

#ordenar el dataframe ordenado por magnitud absoluta
sorted_df = df.sort_values(by='Magnitud Absoluta', ascending=False)

#pintar el dataframe ordenado
print(sorted_df)

#graficar la magnitud absoluta
fig, ax1 = plt.subplots(figsize=(16, 8))

scatter1 = ax1.scatter(sorted_df['Nombre Propio'], sorted_df['Magnitud Absoluta'], color='b', marker='o', label='Magnitud Absoluta')
ax1.set_ylabel('Magnitud Absoluta', color='b')
ax1.tick_params(axis='x', rotation=45, labelsize=8)
ax1.grid(True)

#pintar la luminosidad en la misma tabla
ax2 = ax1.twinx()
scatter2 = ax2.scatter(sorted_df['Nombre Propio'], sorted_df['Luminosidad'], color='r', marker='o', label='Luminosidad')
ax2.set_ylabel('Luminosidad', color='r')

#igualamos los limites del eje x a ambos lados para que la información esté cuadrada
common_xlim = (min(ax1.get_xlim()[0], ax2.get_xlim()[0]), max(ax1.get_xlim()[1], ax2.get_xlim()[1]))
ax1.set_xlim(common_xlim)
ax2.set_xlim(common_xlim)

#ajustar el texto del eje x para que no se sobrepongas
plt.xticks(rotation=45, ha='right', fontsize=6)
fig.autofmt_xdate(rotation=45)

#combinar las etiquetas de ambas gráficas
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper left')

plt.show()
