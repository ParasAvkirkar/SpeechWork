import sounddevice as sd
import numpy as np


fs = 48000
duration = 10  # seconds
print("Listening started")
myrecording = sd.rec(duration * fs, samplerate=fs, channels=2, blocking=True)
print("Listening finished")

sd.default.samplerate = fs
sd.default.channels = 2
print(str(type(myrecording)))

print("Playback started")
sd.play(myrecording, fs, blocking=True)
# sd.play(myarray, fs)