from scipy.signal import butter, lfilter
import numpy as np
def butter_bandstop_filter(data, lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='bandstop')
    y = lfilter(b, a, data)
    return y

# Exemple d'utilisation :

fs = 6000.0       # fréquence d'échantillonnage
lowcut = 500.0    # fréquence de coupure basse
highcut = 1500.0  # fréquence de coupure haute
order = 6         # ordre du filtre

# Création d'un signal test
T = 0.1
nsamples = T * fs
t = np.arange(0, nsamples) / fs
a = 0.02
f = 600.0
x = 0.1 * np.sin(2 * np.pi * 1.2 * np.sqrt(t))
x += 0.01 * np.cos(2 * np.pi * 312 * t + 0.1)
x += a * np.cos(2 * np.pi * f * t + .11)
x += 0.03 * np.cos(2 * np.pi * 2000 * t)

# Application du filtre
y = butter_bandstop_filter(x, lowcut, highcut, fs, order)

# Vous pouvez visualiser le signal avant et après le filtrage en utilisant matplotlib
import matplotlib.pyplot as plt
plt.figure()
plt.plot(t, x, label='Signal Original')
plt.plot(t, y, label='Signal Filtré')
plt.legend()
plt.show()