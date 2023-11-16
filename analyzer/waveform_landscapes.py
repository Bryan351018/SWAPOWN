'''
Tools to generate mesh landscapes of parameterized waveforms
'''

import numpy as np

# Old version

# def generate_landscape(wave, freq, p_range, x_samp_rate):
#     '''
#     Generate a 3D mesh of a parameterized wave.

#     ARGUMENTS
#     wave: The wave function f(x, p)
#     freq: The frequency of the plotted waves
#     p_range: An ndarray of all p values which the mesh needs to contain
#     x_samp_rate: Sample rate of the x values

#     RETURN VALUE
#     A tuple (p_mesh, x_mesh, y_mesh) that can be passed and indexed into matplotlib for surface plotting
#     '''
#     # Get period
#     period = 1 / freq

#     # Get x range
#     x_range = np.linspace(0, period, x_samp_rate)

#     # Generate px mesh
#     ps, xs = np.meshgrid(p_range, x_range)

#     # Reshape p array for evaluating wave function
#     p_nested = ps.reshape(ps.size, 1)

#     # Evaluate functions for all ps and xs
#     ys_raw = wave(x_range, p_nested)

#     return (ps, xs, ys_raw)

def generate_landscape(wave, x_range, p_range):
    '''
    Generate a 3D mesh of a parameterized wave (does not support noise).

    ARGUMENTS
    wave: The wave function f(x, p)
    x_range: An ndarray of all x values which the mesh needs to contain
    p_range: An ndarray of all p values which the mesh needs to contain

    RETURN VALUE
    A tuple (p_mesh, x_mesh, y_mesh) that can be passed and indexed into matplotlib for surface plotting
    '''

    # Generate px mesh
    ps, xs = np.meshgrid(p_range, x_range)

    # Evaluate functions for all ps and xs
    ys_raw = wave(xs, ps)

    return (ps, xs, ys_raw)
