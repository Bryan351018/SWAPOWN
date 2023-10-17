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

# Frequency
waveforms.freq = 440

# Amplitude
waveforms.amp = np.iinfo(SOUND_FORMAT).max / 4

# Sound output X list
xlist_sound = np.linspace(0., 1., SAMPLE_RATE)

# Sound output Y lists
y_squ_sound = waveforms.rect_osc(xlist_sound)
y_pul_sound = waveforms.rect_osc(xlist_sound, 0.1)
y_sin_sound = waveforms.sin_osc(xlist_sound)
y_tri_sound = waveforms.tri_osc(xlist_sound)
y_saw_sound = waveforms.saw_osc(xlist_sound)
y_noise_sound = waveforms.noise(xlist_sound)

def save_sound(name: str, data) -> None:
    with open(f"{OUT_DIR}/{name}.wav", "wb") as handle:
        write_sound(handle, SAMPLE_RATE, data.astype(SOUND_FORMAT))

save_sound("square", y_squ_sound)
save_sound("pulse", y_pul_sound)
save_sound("sine", y_sin_sound)
save_sound("triangle", y_tri_sound)
save_sound("saw", y_saw_sound)
save_sound("noise", y_noise_sound)
