'''
Output sound files
'''

import numpy as np
from analyzer import waveforms
from scipy.io.wavfile import write as write_sound
from os.path import dirname

# Output directory
OUT_DIR = dirname(__file__) + "/../outputs"

# Sound file sample rate
SAMPLE_RATE = 44100

# Sound file format
SOUND_FORMAT = np.int32

# Number of periods
NUM_PERIODS = 800

# Number of parameter changes (for parameterized sweeps)
NUM_P_CHANGES = 853

# Frequency
waveforms.freq = 440

# Audio file length
sound_duration = NUM_PERIODS / waveforms.freq

# Amplitude
waveforms.amp = int(np.iinfo(SOUND_FORMAT).max / 8)

# Sound output X list
xlist_sound = np.linspace(0., sound_duration, np.round(sound_duration * SAMPLE_RATE).astype(np.int32))

# Unidirectional sweep function to output parameterized sounds
def sweep(wave, pmin, pmax, steps):
    # List of x lists
    x_lists = np.split(xlist_sound, steps)
    x_lists = np.array(x_lists)
    
    # Parameter list
    p_list = np.linspace(pmin, pmax, steps)
    p_list = p_list.reshape((-1, 1)).repeat(x_lists.shape[1], axis=1)

    # List of y lists
    y_lists = wave(x_lists, p_list)

    # Y list
    y_list = np.reshape(y_lists, -1)

    return y_list

# Bidirectional sweep function
def bi_sweep(wave, pmin, pmax, steps):
    y_forward = sweep(wave, pmin, pmax, steps)
    y_backward = sweep(wave, pmax, pmin, steps)
    return np.concatenate((y_forward, y_backward))

# Sound output Y lists
# y_squ_sound = waveforms.rect_osc(xlist_sound)
# y_pul_sound = waveforms.rect_osc(xlist_sound, 0.1)
# y_sin_sound = waveforms.sin_osc(xlist_sound)
# y_tri_sound = waveforms.tri_osc(xlist_sound)
# y_saw_sound = waveforms.saw_osc(xlist_sound)
# y_noise_sound = waveforms.noise(xlist_sound)

def save_sound(name: str, data) -> None:
    with open(f"{OUT_DIR}/{name}.wav", "wb") as handle:
        write_sound(handle, SAMPLE_RATE, data.astype(SOUND_FORMAT))

# save_sound("square", y_squ_sound)
# save_sound("pulse", y_pul_sound)
# save_sound("sine", y_sin_sound)
# save_sound("triangle", y_tri_sound)
# save_sound("saw", y_saw_sound)
# save_sound("noise", y_noise_sound)

saw_tri_sw = bi_sweep(waveforms.saw_tri, 0, 1, NUM_P_CHANGES)
pul_sqr_sw = bi_sweep(waveforms.pul_sqr, 0, 1, NUM_P_CHANGES)
tri_sqr_sw = bi_sweep(waveforms.tri_sqr, 0, 1, NUM_P_CHANGES)
noise_sw = bi_sweep(waveforms.noise, 400, 6400, NUM_P_CHANGES)
save_sound("saw_tri_sw", saw_tri_sw)
save_sound("pul_sqr_sw", pul_sqr_sw)
save_sound("tri_sqr_sw", tri_sqr_sw)
save_sound("noise_sw", noise_sw)
