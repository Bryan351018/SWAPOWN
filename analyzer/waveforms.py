'''
Test waveforms that will go through fourier analysis later
'''

import numpy as np
from numpy.random import default_rng
from scipy.signal import square, sawtooth


freq: float
'''The frequency'''

amp: float
'''The amplitude'''

# Shift by a quarter period
def shift_QP(x, freq):
    return (x + 1 / (4 * freq))

# Shift by a half period
def shift_HP(x, freq):
    return (x + 1 / (2 * freq))

# Shift dynamically (for a sawtooth-triangle oscillator)
def shift_dynam(x, freq, p):
    return (x + (2 - p) / (4 * freq))

# 1. Basic waveforms

def sin_osc(x):
    '''Sine oscillator'''
    return amp * np.sin(2 * np.pi * freq * x)

def tri_osc(x):
    '''Triangle oscillator'''
    return amp * sawtooth(2 * np.pi * freq * shift_QP(x, freq), 0.5)

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
    return amp * square(2 * np.pi * freq * x, duty)

def saw_osc(x):
    '''Sawtooth oscillator'''
    return amp * sawtooth(2 * np.pi * freq * shift_HP(x, freq))



# 2. Parameterized oscillators
def pul_sqr(x, p):
    '''Rectangular oscillator with duty parameterized from 0 to 1'''
    return rect_osc(x, p)

def tri_sqr(x, p):
    '''Triangle-to-square oscillator with morph parameterized from 0 to 1'''
    # Quarter-period
    QP = 1 / (4 * freq)

    # Half-flat-edge (half of the peak or trough duration)
    half_flat = QP * p

    # X Modulo period (i.e. stage of a period)
    x_mod_t = np.mod(x, 1 / freq)

    # Rising line slope
    rise = amp / (1 / ((4 * freq) - p / 2))

    # return np.piecewise(x_mod_t, 
    # [
    #     np.logical_and(x_mod_t >= 0, x_mod_t < QP - p / 2), # First rise
    #     np.logical_and(x_mod_t >= QP - p / 2, x_mod_t < QP + p / 2), # Steady peak
    #     np.logical_and(x_mod_t >= QP + p / 2, x_mod_t < 3 * QP - p / 2), # Fall
    #     np.logical_and(x_mod_t >= 3 * QP - p / 2, x_mod_t < 3 * QP + p / 2), # Steady trough
    #     np.logical_and(x_mod_t >= 3 * QP + p / 2, x_mod_t < 4 * QP) # Second rise
    # ],
    # [
    #     lambda x_mod_t: x_mod_t * rise, # First rise
    #     amp, # Steady peak
    #     lambda x_mod_t: (x_mod_t - (QP + p / 2)) * -rise, # Fall
    #     -amp, # Steady trough
    #     lambda x_mod_t: (x_mod_t - (3 * QP + p / 2)) * rise # Second rise
    # ])

    # Alternative implementation with select

    # Condition lists
    conds = [
        np.logical_and(x_mod_t >= 0, x_mod_t < QP - half_flat), # First rise
        np.logical_and(x_mod_t >= QP - half_flat, x_mod_t < QP + half_flat), # Steady peak
        np.logical_and(x_mod_t >= QP + half_flat, x_mod_t < 3 * QP - half_flat), # Fall
        np.logical_and(x_mod_t >= 3 * QP - half_flat, x_mod_t < 3 * QP + half_flat), # Steady trough
        np.logical_and(x_mod_t >= 3 * QP + half_flat, x_mod_t < 4 * QP) # Second rise
    ]

    # Function lists
    funcs = [
        x_mod_t * rise, # First rise
        amp, # Steady peak
        amp - (x_mod_t - (QP + half_flat)) * rise, # Fall
        -amp, # Steady trough
        -amp + (x_mod_t - (3 * QP + half_flat)) * rise # Second rise
    ]

    return np.select(conds, funcs)


def saw_tri(x, p):
    '''Saw-to-triangle oscillator with morph parameterized from 0 to 1'''
    return amp * sawtooth(2 * np.pi * freq * shift_dynam(x, freq, p), 1 - p / 2)

# 3. White noise (old implementation)
def noise(x, gen_freq=None):
    '''
    White noise generator

    OPTIONAL ARGUMENT:
    gen_freq: the generation frequency (overrides analyzer.freq)
    '''
    # Get generation period (use gen_freq if available, else freq)
    period = 1 / (gen_freq[0] if gen_freq is not None else freq)

    # Create random number generator
    rng = default_rng()

    # Amount of random numbers to get
    rand_amt = None
    if type(period) == "float":
        rand_amt = int(np.amax(x) // period)
    else:
        rand_amt = np.maximum(np.amax(x) // period, 1).astype(int)



    # Get all random numbers
    rand = rng.uniform(-amp, amp, np.sum(rand_amt))

    # Index array start bounds
    index_starts = np.add.accumulate(rand_amt.flat)
    index_starts = np.insert(index_starts, 0, 0)
    index_starts = np.delete(index_starts, -1)


    # # Get repeats per full generation period
    # rep = np.maximum(period // (x[1] - x[0]), 1).astype("int64").reshape(-1)

    # Make index arrays
    indexarr = np.linspace(index_starts, index_starts + rand_amt.flat - 1, x.shape[0])
    # indexarr = np.transpose(indexarr)
    indexarr = np.floor(indexarr)

    # Make filled random number arrays
    filled_arr = rand[indexarr.astype("int64")]

    return filled_arr

    # # Stretch some random samples evenly to 
    # def stretch(rands, source):
    #     pass

    # # Array of repeat times

    # a. 
    

    # # b. Get number of remainder repeats
    # rep_rem_p = (x.size % rep).reshape(-1)

    # # c. Get number of full repeat periods
    # rep_full_p = rand_amt - np.sign(rep_rem_p)

    # # c. Interleave
    # def interleave(a, b, loc):
    #     c = np.insert(a, loc, b)
    #     return c

    # rep_list = interleave(np.repeat(rep, rep_full_p), rep_rem_p, np.add.accumulate(rep_full_p))

    # # d. Repeat
    # res = np.repeat(rand, rep_list).reshape(x.size, -1)

    # # # Half-baked result
    # # res = np.repeat(rand.flat, rep.flat)[:x.size]

    # # # Append missing elements
    # # if res.size:
    # #     res = np.append(res, np.repeat(res[-1], x.size - res.size))
    # # # If there's no elements at all, add an element
    # # else:
    # #     res = (rng.random(1) - 0.5) / 0.5 * amp
    
    # return res

# def noise(x, gen_freq=None):
#     '''
#     White noise generator

#     OPTIONAL ARGUMENT:
#     gen_freq: the generation frequency (overrides analyzer.freq)
#     '''

#     # Get active frequency variable
#     f = gen_freq if gen_freq is not None else freq

#     # Get generation period (use gen_freq if available, else freq)
#     period = 1 / f

#     # Construct pandas timedelta object
#     pd_delta = pd.Timedelta(period, "sec")

#     # Create random number generator
#     rng = default_rng()

#     # Amount of random numbers to get
#     rand_amt = None
#     if type(period) == "float":
#         rand_amt = int(np.amax(x) // period)
#     else:
#         rand_amt = (np.amax(x) // period).astype(int).reshape(-1)

#     # Get all random numbers
#     rand = rng.uniform(-amp, amp, np.sum(rand_amt))

#     # Construct pandas series object
#     pd_series = pd.Series(rand, pd.interval_range(start=x[0], end=x[-1], freq=f))

#     pd_series = pd_series.resample(pd_delta)


# Test
def test_sine(x, p):
    return np.sin(2 * np.pi * (p * 2000 + 2000) * x)
