'''
Functions that actually perform fourier analysis
'''

import numpy as np
from scipy.fft import fft, fftfreq

def get_trans_x(n, dt):
    '''
    Fourier transform get x values

    ARGUMENTS
    n: number of samples
    dt: time step between the samples

    RETURN VALUE
    An ndarray containing the transform x values (frequencies)
    '''
    return fftfreq(n, dt)[:n//2]

# Old version

# def get_trans_y(y, n):
#     '''
#     Fourier transform get y values

#     ARGUMENTS
#     y: the wave
#     n: number of samples

#     RETURN VALUE
#     An ndarray containing the transform y values (amplitudes)
#     '''
#     full_ys = fft(y)
#     full_ys = np.delete(full_ys, np.s_[0:n//2], axis=1)
#     full_ys = 2 * np.abs(full_ys) / n

#     return full_ys

def get_trans_y(y, n):
    '''
    Fourier transform get y values

    ARGUMENTS
    y: the wave
    n: number of samples

    RETURN VALUE
    An ndarray containing the transform y values (amplitudes)
    '''
    full_ys = fft(y, axis=0)
    full_ys = np.take(full_ys, indices=range(n // 2), axis=0)
    full_ys = 2 * np.abs(full_ys) / n

    return full_ys



def decomp(y, n, dt):
    '''
    Get the fourier transform results for an unparameterized wave.

    ARGUMENTS
    y: the wave
    n: number of samples
    dt: time step between the samples

    RETURN VALUE
    A tuple (tx, ty), 
    where tx is the transform x values (frequencies), 
    and ty is the transform y values (amplitudes)
    '''

    return (get_trans_x(n, dt), get_trans_y(y, n))

# Old version

# def decomp_param(func, x, p, n, dt):
#     '''
#     Get the fourier transform results for a parameterized wave.

#     ARGUMENTS
#     func(x, p): the wave function that accepts x, the list of x values, and p, the list of parameters
#     x: the list of x values
#     p: the list of parameters (in a single unnested ndarray)
#     n: number of samples
#     dt: time step between the samples

#     RETURN VALUE
#     A tuple (p, tx, ty), 
#     where p is the list of parameters,
#     tx is the transform x values (frequencies), 
#     and ty is the transform y values (amplitudes)
#     '''
#     # Reshape the parameters aray for post-processing
#     p_nested = p.reshape(p.size, 1)

#     # Get y values of wave function parameterized by p
#     wave_ys = func(x, p_nested)

#     # Transform x values
#     trans_x = np.array([get_trans_x(n, dt)])
#     trans_x = np.repeat(trans_x, p.size, axis=0)

#     # Transform y values
#     trans_y = get_trans_y(wave_ys, n)

#     # Pretty-formatted repeated p array
#     pretty_p = np.repeat(p_nested, n // 2, axis=1)

#     # Transpose everything
#     pretty_p = np.transpose(pretty_p)
#     trans_x = np.transpose(trans_x)
#     trans_y = np.transpose(trans_y)

#     return (pretty_p, trans_x, trans_y)

def decomp_param(func, x, p, n, dt, normalized=True):
    '''
    Get the fourier transform results for a parameterized wave.

    ARGUMENTS
    func(x, p): the wave function that accepts x, the list of x values, and p, the list of parameters
    x: the list of x values
    p: the list of parameters (in a single unnested ndarray)
    n: number of samples
    dt: time step between the samples
    normalized: whether to output [1,2,...] instead of frequency values in frequency output

    RETURN VALUE
    A tuple (p, tx, ty), 
    where p is the list of parameters,
    tx is the transform x values (frequencies), 
    and ty is the transform y values (amplitudes)
    '''
    # Reshape the parameters aray for post-processing
    p_nested = p.reshape(p.size, 1)

    # Generate px mesh
    ps, xs = np.meshgrid(p, x)

    # Get y values of wave function parameterized by p
    wave_ys = func(xs, ps)

    # Transform x values
    trans_x = np.array([get_trans_x(n, dt)])
    trans_x = np.repeat(trans_x, p.size, axis=0)
    # Transpose it
    trans_x = np.transpose(trans_x)

    # Transform y values
    trans_y = get_trans_y(wave_ys, n)

    # Pretty-formatted repeated p array
    pretty_p = np.repeat(p_nested, n // 2, axis=1)
    # Transpose it
    pretty_p = np.transpose(pretty_p)    
    # trans_y = np.transpose(trans_y)

    # Normalization
    if normalized:
        trans_x /= trans_x[1][0]

    return (pretty_p, trans_x, trans_y)
