from flask import Flask, jsonify 
from flask_cors import CORS, cross_origin
import brainflow
import numpy as np
from midiutil import MIDIFile

import pandas as pd
import matplotlib.pyplot as plt

import os 
import requests
from dotenv import load_dotenv
from Billboard import Billboard 

from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations, WindowOperations, DetrendOperations, NoiseTypes


load_dotenv() 

spotify_client_id = os.getenv('CLIENT_ID')
spotify_client_secret = os.getenv('CLIENT_SECRET')
user_id = os.getenv("USER_ID")
authorization_url = "https://accounts.spotify.com/authorize"
redirect_uri = "https://example.com/callback"
token_url = "https://accounts.spotify.com/api/token"
creation_playlist_endpoint = f"https://api.spotify.com/v1/users/{user_id}/playlists"

scope = "playlist-modify-public playlist-modify-private"


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
    if mood == "deep sleep" or "creative/meditative" or "relaxed/focused":
        return "calm" 
    elif mood == "active/stressed":
        return "anxious"
    elif mood == "high cognitive processing":
        return "happy"

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
@app.route('/generate-prompt', methods=['GET'])
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
    spotify_prompt = generate_music_prompt(mood)
    
    try:
        response = requests.post('http://localhost:5001/receive-mood', json={'mood': spotify_prompt})
        if response.status_code != 200:
            print("Error sending mood to Spotify service")
        # Handle error appropriately
    except requests.RequestException as e:
        print(f"Request failed: {e}")
    # Handle exception

    
    print(prompt)
    print(spotify_prompt)
    return jsonify({'prompt': prompt}), jsonify({'prompt': prompt, 'spotify_prompt': spotify_prompt})


if __name__ == "__main__":
    app.run(debug=True)
