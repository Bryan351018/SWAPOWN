'''
Test waveforms that will go through fourier analysis later
'''

from numpy import sin, pi, repeat, amax, append
from numpy.random import default_rng
from scipy.signal import square, sawtooth


freq: float
'''The frequency'''

amp: float
'''The amplitude'''


# 1. Basic waveforms

def sin_osc(x):
    '''Sine oscillator'''
    return amp * sin(2 * pi * freq * x)

def tri_osc(x):
    '''Triangle oscillator'''
    return amp * sawtooth(2 * pi * freq * x, 0.5)

"""
Square wave older implementation

def squ_osc(x: float) -> float:
    '''Square oscillator'''
    # Calculate 1/2 period
    period = 0.5 * (1 / freq)

    # Calculate 1/2 period zone that x is in
    period_zone = x // period

    # Calculate the zone modulus (0 = upper edge, 1 = lower edge)
    zone_mod = period_zone % 2

    # Convert moduli (0, 1) to unit directions (-1, 1)

    # Step 1: (0, 1) -> (0, 2)
    zone_mod *= 2

    # Step 2: (0, 2) -> (-1, 1)
    zone_mod -= 1

    # Step 3: (-1, 1) -> (amp, -amp)
    zone_mod *= -amp

    return zone_mod
"""
def rect_osc(x, duty: float = 0.5):
    '''Rectangular oscillator with mutable duty'''
    return amp * square(2 * pi * freq * x, duty)

def saw_osc(x):
    '''Sawtooth oscillator'''
    return amp * sawtooth(2 * pi * freq * x)



# 2. Parameterized oscillators


# 3. White noise
def noise(x):
    '''White noise generator'''
    # Get generation period
    period = 1 / freq

    # Create random number generator
    rng = default_rng()

    # Get random numbers
    rand = (rng.random(int(amax(x) // period)) - 0.5) / 0.5 * amp

    # Half-baked result
    res = repeat(rand, max(period // (x[1] - x[0]), 1))[:x.size]

    # Append missing elements
    if res.size:
        res = append(res, repeat(res[-1], x.size - res.size))
    # If there's no elements at all, add an element
    else:
        res = (rng.random(1) - 0.5) / 0.5 * amp
    
    return res
