import pandas as pd
import numpy as np
import csv
import re
import matplotlib.pyplot as plt

# Create a list for the values of Magnitud Absoluta
List = []

# Create a list to store 'Nombre Propio' values
nombre_propio_list = []

# Function to convert the string to float, handling the non-standard minus sign
def convert_to_float(value):
    value = value.replace(',', '.')  # Replace commas with dots for correct conversion
    return float(re.sub('[^0-9eE.+-]', '', value.replace('−', '-')))

try:
    # Open the CSV file in read mode with explicit encoding
    with open('Tabla.csv', 'r', encoding='utf-8') as file:
        # Use the CSV reader to read the content and skip lines with different numbers of fields
        csv_reader = csv.reader(file)
        header = next(csv_reader)  # Get the header

        # Identify the 'Nombre Propio' column index case-insensitively
        nombre_propio_index = next((i for i, col in enumerate(header) if col.strip().lower() == 'nombre propio'), None)

        if nombre_propio_index is None:
            raise ValueError("Column 'Nombre Propio' not found in the CSV header.")

        for row in csv_reader:
            # Skip lines with a different number of fields
            if len(row) != len(header):
                continue

            # Process each row as needed
            print(row)

            # Access specific columns by their index
            magnitud_aparente = convert_to_float(row[1])
            distancia_años_luz = convert_to_float(row[4])  # Replace non-standard minus sign

            # Calculate magnitud absoluta and append to the list
            distancia_parsecs = distancia_años_luz / 3.2616
            magnitud_absoluta = magnitud_aparente - 5 * (np.log10(distancia_parsecs) - 1)
            List.append(magnitud_absoluta)

            # Get 'Nombre Propio' value and append to the list
            nombre_propio_value = row[nombre_propio_index]
            nombre_propio_list.append(nombre_propio_value)

except FileNotFoundError:
    print("The specified CSV file was not found.")

except Exception as e:
    print(f"An error occurred: {e}")

# Create a DataFrame from the lists
df = pd.DataFrame({'Nombre Propio': nombre_propio_list, 'Magnitud Absoluta': List})

# Create a new column for "Luminosidad"
df['Luminosidad'] = 10 ** ((4.83 - df['Magnitud Absoluta']) / 2.5)

# Create a new DataFrame with Magnitud Absoluta values and corresponding Nombre Propio
sorted_df = df.sort_values(by='Magnitud Absoluta', ascending=False)

# Display the sorted DataFrame
print(sorted_df)

# Print basic notions in order to read the given information
print("Mientras más baja sea la magnitud absoluta, más brillante es la estrella")
print("Mientras más brillante es la estrella mayor es su luminosidad")

# Plot the Magnitud Absoluta against Nombre Propio for the sorted DataFrame
import matplotlib.pyplot as plt

fig, ax1 = plt.subplots(figsize=(16, 8))

# Scatter plot for Magnitud Absoluta
scatter1 = ax1.scatter(sorted_df['Nombre Propio'], sorted_df['Magnitud Absoluta'], color='b', marker='o', label='Magnitud Absoluta')
ax1.set_ylabel('Magnitud Absoluta', color='b')
ax1.tick_params(axis='x', rotation=45, labelsize=8)
ax1.grid(True)

# Create a twin Axes for Luminosidad
ax2 = ax1.twinx()
scatter2 = ax2.scatter(sorted_df['Nombre Propio'], sorted_df['Luminosidad'], color='r', marker='o', label='Luminosidad')
ax2.set_ylabel('Luminosidad', color='r')

# Synchronize x-axis limits
common_xlim = (min(ax1.get_xlim()[0], ax2.get_xlim()[0]), max(ax1.get_xlim()[1], ax2.get_xlim()[1]))
ax1.set_xlim(common_xlim)
ax2.set_xlim(common_xlim)

# Adjust x-axis labels to prevent overlap
plt.xticks(rotation=45, ha='right', fontsize=6)
fig.autofmt_xdate(rotation=45)  # Additional rotation for better spacing

# Combine legends from both axes
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='upper left')

plt.show()
