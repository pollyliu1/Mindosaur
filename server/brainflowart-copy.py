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

from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations, WindowOperations, DetrendOperations, NoiseTypes
from config import BASE_PROMPT

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
        return "harmonious."
    elif mood == "active/stressed":
        return "energetic."
    elif mood == "high cognitive processing":
        return "vibrant."
    else:
        return


def read_eeg_data_from_file(file_path):
    # Adjust the number of columns according to your file format
    columns = ["Index"] + [f"Channel_{i}" for i in range(8)] + ["Other_data"]
    return pd.read_csv(file_path, skiprows=4, header=None, names=columns)


def get_spotify_token():
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(auth_url, {
        'grant_type': 'client_credentials',
        'client_id': spotify_client_id,
        'client_secret': spotify_client_secret,
    })
    auth_response_data = auth_response.json()
    return auth_response_data['access_token']

def create_spotify_playlist(user_id, token, mood):
    url = f'https://api.spotify.com/v1/users/{user_id}/playlists'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    payload = {
        'name': f'Mood Playlist: {mood}',
        'description': f'Playlist based on mood: {mood}',
        'public': False
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()['id']


def find_songs_for_mood(mood, token):
    # Replace with your logic to find songs based on mood
    # For example, you can use Spotify's search API
    # This is a placeholder function
    return []

def add_songs_to_playlist(playlist_id, songs, token):
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    payload = {
        'uris': songs
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.status_code == 201

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
    
    #Spotify playlist creation
    token = get_spotify_token()
    playlist_id = create_spotify_playlist(spotify_user_id, token, mood)
    songs = find_songs_for_mood(spotify_prompt, token)
    if songs:
        add_songs_to_playlist(playlist_id, songs, token)
    
    
    print(prompt)
    print(spotify_prompt)
    return jsonify({'prompt': prompt}), jsonify({'prompt': prompt, 'spotify_prompt': spotify_prompt})


if __name__ == "__main__":
    app.run(debug=True)
