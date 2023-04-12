import numpy as np

# Créer des données de signal fictives
signal = np.array([0, 1, 2, 1, 0, -1, -2, -1])

# Effectuer la transformée de Fourier
fourier = np.fft.fft(signal)

# Afficher les résultats
print(fourier)

import matplotlib.pyplot as plt

# Trouver l'amplitude de chaque composante fréquentielle
amplitude = np.abs(fourier)

# Tracer le résultat
plt.plot(amplitude)
plt.show()
