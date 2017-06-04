import sounddevice as sd
import numpy as np


fs = 48000
duration = 10  # seconds
myrecording = sd.rec(duration * fs, samplerate=fs, channels=2, blocking=True)

sd.default.samplerate = fs
sd.default.channels = 2



sd.play(myrecording, fs, blocking=True)
# sd.play(myarray, fs)