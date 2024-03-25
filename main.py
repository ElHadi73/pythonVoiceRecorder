import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import keyboard  # for key detection
import time
import threading

def timer():
        while(True):
            i = 0
            mins, secs = divmod(i, 60)
            time_format = '{:02d}:{:02d}'.format(mins, secs)
            print(time_format, end='\r')
            time.sleep(1)

def record_until_keypress(fs=44100, channels=2, filename='output_until_keypress.wav'):
    """
    Record audio from the microphone until a key press and save it to a WAV file.

    Args:
    - fs: Sampling frequency (default 44100Hz).
    - channels: Number of audio channels (default is 2 for stereo).
    - filename: Name of the file to save the recording.
    """
    print("Recording... Press 'q' to stop.")

    # Define a callback function for the recording
    def callback(indata, frames, time, status):
        recording.append(indata.copy())
        if keyboard.is_pressed('q'):  # Stop recording when 'q' is pressed
            raise sd.CallbackAbort

    # Empty list to store recorded data
    recording = []

    try:
        # Start recording
        with sd.InputStream(callback=callback, samplerate=fs, channels=channels):
            sd.sleep(1000000)  # Wait a long time until aborted
    except KeyboardInterrupt:
        print('Recording stopped by user')
    except sd.CallbackAbort:
        print('Recording stopped.')
    finally:
        # Convert list to NumPy array and save as WAV file
        recording_array = np.concatenate(recording, axis=0)
        write(filename, fs, recording_array)
        print(f"Recording saved as '{filename}'")

# Example usage
record_until_keypress()
