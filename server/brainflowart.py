from flask import Flask, jsonify, Blueprint
from flask_cors import CORS, cross_origin
import brainflow
import numpy as np
from midiutil import MIDIFile

import pandas as pd
import matplotlib.pyplot as plt

import os 
import requests
from dotenv import load_dotenv


from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations, WindowOperations, DetrendOperations, NoiseTypes

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

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
    if mood == "deep sleep":
        return "soft"
    elif mood == "creative/meditative":
        return "classical"
    elif mood == "relaxed/focused":
        return "harmonious"
    elif mood == "active/stressed":
        return "energetic"
    elif mood == "high cognitive processing":
        return "vibrant"
    else:
        return

def generate_facials_prompt(mood):
    mood_to_numeric = {
        "deep sleep": 0,                # calm
        "creative/meditative": 0,       # calm
        "relaxed/focused": 0,           # calm
        "active/stressed": 1,           # anxious
        "high cognitive processing": 2  # happy
    }

    return mood_to_numeric.get(mood, 0)  # Default to 0 (calm) if mood is not found


def read_eeg_data_from_file(file_path):
    # Adjust the number of columns according to your file format
    columns = ["Index"] + [f"Channel_{i}" for i in range(8)] + ["Other_data"]
    return pd.read_csv(file_path, skiprows=4, header=None, names=columns)

    # Define keywords for each mood to search for songs
    mood_keywords = {
        "deep sleep": "calm",
        "creative/meditative": "meditative",
        "relaxed/focused": "relaxing",
        "active/stressed": "energetic",
        "high cognitive processing": "intense"
    }

    # Default keyword if mood is unknown or not in the dictionary
    keyword = mood_keywords.get(mood, "music")


# Flask route to generate prompt
@app.route('/g-prompt', methods=['GET'])
@cross_origin()
def generate_prompt():
    file_path = './OpenBCI_GUI-v5-meditation_copy.txt'
    eeg_data = (read_eeg_data_from_file('./OpenBCI_GUI-v5-meditation_copy.txt'))
    sampling_rate = 250 

    
     # Assuming the first EEG channel is 'Channel_0', modify as per your data
    eeg_channel_data = eeg_data["Channel_0"].values

    # Data filtering
    DataFilter.perform_bandpass(eeg_channel_data, sampling_rate, 1.0, 30.0, 4, FilterTypes.BUTTERWORTH.value, 0)
    DataFilter.remove_environmental_noise(eeg_channel_data, sampling_rate, NoiseTypes.FIFTY.value)

    
    # Perform FFT and compute PSD
    eeg_channel_data = eeg_channel_data - np.mean(eeg_channel_data)  # Detrend the data
    fft_result = np.fft.fft(eeg_channel_data)
    fft_frequencies = np.fft.fftfreq(len(eeg_channel_data), d=1/sampling_rate)
    psd = np.abs(fft_result) ** 2

    # Infer mood from EEG data
    mood = infer_mood_from_eeg(eeg_channel_data, sampling_rate)
    prompt = generate_artwork_prompt(mood)
    print(prompt)
    return {
        "prompt": prompt
    }
    # return jsonify({'prompt': prompt}), jsonify({'prompt': prompt})


if __name__ == "__main__":
    app.run(debug=True)
