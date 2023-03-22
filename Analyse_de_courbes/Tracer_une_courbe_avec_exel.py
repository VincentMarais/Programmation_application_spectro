import pandas as pd
import matplotlib.pyplot as plt

# Lire le fichier ODS
data = pd.read_excel("Manip\Manip_22_03_2023\expérience_1_echantillon.ods", engine="odf")

# Obtenir les colonnes D et E
col_D = data['Longueur donde']
col_E = data['log']

# Tracer le graphe
plt.plot(col_D, col_E)
plt.xlabel('Nombre de point')
plt.ylabel('Absorbance ')
plt.title('Absorbance du bromophenol')
plt.show()
