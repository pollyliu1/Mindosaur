import time
import requests
import brainflow
import numpy as np
from midiutil import MIDIFile

import pandas as pd
import matplotlib.pyplot as plt

from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations, WindowOperations, DetrendOperations, NoiseTypes
from config import BASE_PROMPT

# functions for mood inference and prompt generation
def infer_mood_from_eeg(data, sampling_rate):
    # Perform FFT on the EEG data
    fft_result = np.fft.fft(data)
    fft_frequencies = np.fft.fftfreq(len(data), d=1/sampling_rate)

    # Compute the power spectral density (PSD)
    psd = np.abs(fft_result) ** 2

    # Find the predominant frequency band
    dominant_frequency = fft_frequencies[np.argmax(psd)]

    # Infer mood based on the predominant frequency band
    if 0.5 <= dominant_frequency < 3:
        return "deep sleep"
    elif 3 <= dominant_frequency < 8:
        return "creative/meditative"
    elif 8 <= dominant_frequency < 12:
        return "relaxed/focused"
    elif 12 <= dominant_frequency < 30:
        return "active/stressed"
    elif 30 <= dominant_frequency < 100:
        return "high cognitive processing"
    else:
        return "unknown"
    

def generate_artwork_prompt(mood):
    if mood == "deep sleep":
        return "Create an abstract artwork that captures the essence of a dreamy, ethereal, and surreal landscape."
    elif mood == "creative/meditative":
        return "Generate an abstract image that embodies tranquility and mystical imagination."
    elif mood == "relaxed/focused":
        return "Design an abstract harmonious and serene artwork that reflects a state of balance and calmnesss."
    elif mood == "active/stressed":
        return "Produce an abstract dynamic and intense piece of art that resonates with vivid emotions and energy."
    elif mood == "high cognitive processing":
        return "Create an abstract complex and vibrant artwork that is thought-provoking and intricate."
    else:
        return "Generate an abstract artwork."
    
MOOD_DETAILS = {
    "deep sleep": "dreamy, ethereal, and surreal",
    "creative/meditative": "tranquil and mystical",
    "relaxed/focused": "harmonious and serene",
    "active/stressed": "dynamic and intense",
    "high cognitive processing": "vibrant"
}

def generate_music_prompt(mood):
    theme = MOOD_DETAILS.get(mood, "an abstract soundscape")  # Default to "an abstract soundscape" if mood not found
    return f"{BASE_PROMPT} The theme is {theme}."


def main():
    params = BrainFlowInputParams()
    params.board_id = BoardIds.CROWN_BOARD.value 
    # params.serial_port = 'COM5'
    params.serial_number = "9bb2e2fad5668286a4b4f407002b4359"
    board_id = params.board_id
    sampling_rate = BoardShim.get_sampling_rate(board_id)

    board = BoardShim(board_id, params)
    board.prepare_session()
    board.start_stream()
    BoardShim.log_message(LogLevels.LEVEL_INFO.value, 'start sleeping in the main thread')

    time.sleep(10)
    data = board.get_board_data()
    board.stop_stream()
    board.release_session()

    eeg_channels = BoardShim.get_eeg_channels(board_id)
    timestamp_channel = BoardShim.get_timestamp_channel(board_id)
    
    # PSD calculation
    nfft = DataFilter.get_nearest_power_of_two(sampling_rate)
    eeg_channel = eeg_channels[0]
    psd = DataFilter.get_psd_welch(data[eeg_channel], nfft, nfft // 2, sampling_rate, WindowOperations.NO_WINDOW.value)
    
    # Plotting before processing
    df = pd.DataFrame(np.transpose(data))
    plt.figure()
    df[eeg_channels[:3]].plot(subplots=True)
    plt.savefig("before_processing.png")

    # Data filtering
    for channel in eeg_channels:
        DataFilter.perform_bandpass(data[channel], sampling_rate, 1.0, 30.0, 4, FilterTypes.BUTTERWORTH.value, 0)
        DataFilter.remove_environmental_noise(data[channel], sampling_rate, NoiseTypes.FIFTY.value)
    
    # Plotting after processing
    df = pd.DataFrame(np.transpose(data))
    plt.figure()
    df[eeg_channels[:3]].plot(subplots=True)
    plt.savefig("after_processing.png")

    # Infer mood from EEG data
    mood = infer_mood_from_eeg(data[eeg_channels[0]], sampling_rate)
    prompt = generate_artwork_prompt(mood)
    print(prompt)
    return prompt

if __name__ == "__main__":
    main()