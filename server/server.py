from flask import Flask, request, jsonify
from brainflowart import main as brainflow_art_main

app = Flask(__name__)

# This is the route to the root of the server
@app.route('/generate-prompt', methods=['GET'])
def generate_prompt():
    prompt = brainflow_art_main() # Run the main function from brainflow-art.py
    return jsonify({'prompt': prompt})

if __name__ == '__main__':
    app.run(debug=True)