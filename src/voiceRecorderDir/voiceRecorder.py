import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import keyboard  # for key detection
import time
import threading

is_recording = True

def timer():
        global is_recording
        i = 0
        while(is_recording):
            mins, secs = divmod(i, 60)
            time_format = '{:02d}:{:02d}'.format(mins, secs)
            print(time_format, end='\r')
            time.sleep(1)
            i = i + 1

def record_until_keypress(fs=44100, channels=2, filename='record.wav'):
    """
    Record audio from the microphone until a key press and save it to a WAV file.

    Args:
    - fs: Sampling frequency (default 44100Hz).
    - channels: Number of audio channels (default is 2 for stereo).
    - filename: Name of the file to save the recording.
    """

    global is_recording
    print("Recording... Press 'Enter' to stop.")

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
            while is_recording:
                sd.sleep(100)  # Wait a long time until aborted
    except Exception as e:
        print(f'Stopped recording due to: {e}')
    finally:
        # Convert list to NumPy array and save as WAV file
        recording_array = np.concatenate(recording, axis=0)
        write(filename, fs, recording_array)
        print(f"Recording saved as '{filename}'")

def stop_recording():
    global is_recording
    input()
    is_recording = False

def start_recording_with_timer():
    # Define threads for recording and timer
    recording_thread = threading.Thread(target=record_until_keypress, args=(44100, 2))
    timer_thread = threading.Thread(target=timer)
    stoping_thread = threading.Thread(target=stop_recording)

    # Start threads
    timer_thread.start()
    recording_thread.start()
    stoping_thread.start()
    
    # Wait for both threads to complete
    recording_thread.join()
    timer_thread.join()
    stoping_thread.join()

start_recording_with_timer()
