'''
Graph all the test waveforms
'''
import numpy as np
import matplotlib.pyplot as plt
from analyzer import waveforms
from os.path import dirname

# Output directory
OUT_DIR = dirname(__file__) + "/../outputs"

# Frequency
waveforms.freq = 20

# Amplitude
waveforms.amp = 20

# 1. Basic waveforms

# X list
xlist = np.linspace(0, 500, 5000)

# Y lists
y_squ = waveforms.rect_osc(xlist)
y_pul = waveforms.rect_osc(xlist, 0.1)
y_sin = waveforms.sin_osc(xlist)
y_tri = waveforms.tri_osc(xlist)
y_saw = waveforms.saw_osc(xlist)

plt.plot(xlist, y_squ)
plt.plot(xlist, y_pul)
plt.plot(xlist, y_sin)
plt.plot(xlist, y_tri)
plt.plot(xlist, y_saw)
plt.savefig(f"{OUT_DIR}/basics.png")

# 2. Parameterized oscillators

# 3. White noise
waveforms.freq = 0.1
y_noise = waveforms.noise(xlist)
plt.plot(xlist, y_noise)
plt.savefig(f"{OUT_DIR}/noise.png")
