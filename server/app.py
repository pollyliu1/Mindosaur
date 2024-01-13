import os # spotify API
import requests
from flask import Flask

app = Flask(__name__)

# Spotify API setup
spotify_api_key = os.getenv('SPOTIFY_API_KEY')
CLIENT_ID = ''
CLIENT_SECRET = ''
REDIRECT_URL = 'http://localhost:5000/callback'

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1'


@app.route('/')
def home():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
