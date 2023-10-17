'''
Graph all the fourier analysis outputs
'''
import numpy as np
from analyzer import waveforms

# X list
xlist = np.linspace(0, 500, 5000)

# Y lists
y_squ = waveforms.rect_osc(xlist)
