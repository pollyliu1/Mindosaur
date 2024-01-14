from dotenv import load_dotenv
from flask import Flask, request, redirect, jsonify
import os
import requests

load_dotenv(".env")
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
authorization_url = "https://accounts.spotify.com/authorize"
redirect_uri = "http://localhost:5000/callback"
scope = "playlist-modify-public playlist-modify-private user-read-private user-read-email"

app = Flask(__name__)

@app.route('/test')
def test():
    return {"test": "test"}

@app.route('/login')
def login():
    return redirect(
        f"{authorization_url}?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope}"
    )

@app.route('/callback')
def callback():
    global access_token
    access_token = request.args.get('code')
    return {"Login": "Success", "Code": access_token}

@app.route('/info')
def info():
    global access_token
    print(access_token)
    headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    response = requests.get('https://api.spotify.com/v1/me', headers=headers)
    print(response.json())
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)
