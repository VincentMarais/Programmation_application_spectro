import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np

style.use('ggplot')

# Generate data for display
t = []  # Time
y = []  # Signal

# Figure configuration


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

# Real-time display
def animate(i):
    ax.clear()
    ax.set_title("Oscilloscope")
    ax.set_xlabel("Temps")
    ax.set_ylabel("Amplitude")
    ax.plot(t[:i], y[:i])  # Plot a different subset at each frame

i = 0
while i < 21:
    t.append(i)
    y.append(i ** 2)
    i += 1
    y.reverse()


# Animation


OHHHH= animation.FuncAnimation(fig, animate, interval=50)


plt.show()


