'''
Graph all the test waveforms
'''
import numpy as np
import matplotlib.pyplot as plt
from analyzer import waveforms
from os.path import dirname

# Output directory
OUT_DIR = dirname(__file__) + "/../outputs"

# Set graph theme
plt.style.use('dark_background')
# Set graph axis labels
plt.xlabel("x")
plt.ylabel("y")
# Set graph title
plt.title("A Square Wave")

# Frequency
waveforms.freq = 200

# Amplitude
waveforms.amp = 1

# Y axis margin from extrema of wave
Y_MARGIN = 0.1

# Set graph axis range
plt.axis([0, 1 / waveforms.freq, -waveforms.amp - Y_MARGIN, waveforms.amp + Y_MARGIN])

# Sample rate
SAMP_RATE = 8000

# Terminating value of X list
SAMP_END = 100

# Number of samples
num_samp = SAMP_RATE * SAMP_END

# X list
xlist = np.linspace(0, SAMP_END, num_samp)

# 1. Basic waveforms

# Y lists
# y_squ = waveforms.rect_osc(xlist)
# y_pul = waveforms.rect_osc(xlist, 0.1)
# y_sin = waveforms.sin_osc(xlist)
# y_tri = waveforms.tri_osc(xlist)
# y_saw = waveforms.saw_osc(xlist)

# plt.plot(xlist, y_squ)
# plt.plot(xlist, y_pul)
# plt.plot(xlist, y_sin)
# plt.plot(xlist, y_tri)
# plt.plot(xlist, y_saw)
# plt.savefig(f"{OUT_DIR}/squ.png")

# 2. Parameterized oscillators

# 3. White noise
# waveforms.freq = 0.1
# y_noise = waveforms.noise(xlist)
# plt.plot(xlist, y_noise)
# plt.savefig(f"{OUT_DIR}/noise.png")
