'''
Graph all the fourier analysis outputs
'''
import numpy as np
from analyzer import waveforms, decomposer
import matplotlib.pyplot as plt
from matplotlib import cm
from os.path import dirname
from analyzer.waveform_landscapes import generate_landscape
from math import ceil, pi

# Output directory
OUT_DIR = dirname(__file__) + "/../outputs"

# Set graph theme
plt.style.use('dark_background')
# Set graph axis labels
# plt.xlabel("n")
# plt.ylabel("b_n")
# Set graph title
# plt.title("Fourier Series of a Sine Wave")



# Amplitude
waveforms.amp = 1.0

# Frequency
waveforms.freq = 1 / (2 * pi)

# Sample rate
SAMP_RATE = 10

# Periods of wave to analyze
SAMP_PERIODS = 1

# Terminating value of X list
SAMP_END = 1 / waveforms.freq * SAMP_PERIODS

# Number of samples
num_samp = ceil(SAMP_RATE * SAMP_END)

# X list
xlist = np.linspace(0, SAMP_END, num_samp)

# Sample time step
dt = 1 / SAMP_RATE

# Y lists
# y_squ = waveforms.rect_osc(xlist)
# y_pul = waveforms.rect_osc(xlist, 0.1)
# y_sin = waveforms.sin_osc(xlist)
# y_tri = waveforms.tri_osc(xlist)
# y_saw = waveforms.saw_osc(xlist)
# y_noise = waveforms.noise(xlist)

# Analyze
# squ_trans = decomposer.decomp(y_squ, num_samp, dt)
# pul_trans = decomposer.decomp(y_pul, num_samp, dt)
# sin_trans = decomposer.decomp(y_sin, num_samp, dt)
# tri_trans = decomposer.decomp(y_tri, num_samp, dt)
# saw_trans = decomposer.decomp(y_saw, num_samp, dt)
# noise_trans = decomposer.decomp(y_noise, num_samp, dt)

# Graph
# plt.plot(squ_trans[0], squ_trans[1])
# plt.plot(pul_trans[0], pul_trans[1])
# plt.plot(sin_trans[0], sin_trans[1])
# plt.plot(tri_trans[0], tri_trans[1])
# plt.plot(saw_trans[0], saw_trans[1])
# plt.plot(noise_trans[0], noise_trans[1])

# plt.show()
# plt.savefig(f"{OUT_DIR}/sin_transform.png")

# Decompose noise
# x_p_noise = np.linspace(100, 1000, 4)
# trans = decomposer.decomp_param(waveforms.noise, xlist, x_p_noise, num_samp, dt)

# Decompose parameterized square
# x_p_pulsqr = np.linspace(0, 1, 20)
# trans = decomposer.decomp_param(waveforms.pul_sqr, xlist, x_p_pulsqr, num_samp, dt)

x_p_sawtri = np.linspace(0, 1, 30)
trans = decomposer.decomp_param(waveforms.saw_tri, xlist, x_p_sawtri, num_samp, dt)
# trans = decomposer.decomp_param(waveforms.test_sine, xlist, x_p_sawtri, num_samp, dt)
# saw_tri_land = generate_landscape(waveforms.tri_sqr, xlist, x_p_sawtri)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

# px plane size
# PXPLANE_LEN = 5
# p_mesh, x_mesh = np.meshgrid(range(PXPLANE_LEN), range(PXPLANE_LEN))
# ax.plot_surface(p_mesh, x_mesh, np.zeros_like(p_mesh))

# Plot the main graph
surf = ax.plot_surface(trans[0], trans[1], trans[2], cmap="binary")
# ax.plot_surface(saw_tri_land[0], saw_tri_land[1], saw_tri_land[2], cmap="binary")

# fig.colorbar(surf, shrink=0.5, aspect=5)


ax.set_xlabel("p")
ax.set_ylabel("n")
ax.set_zlabel("|A|")

plt.show()
