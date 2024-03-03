from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image

load_dotenv()  # load all the environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  # configure the Google API

app = Flask(__name__)
CORS(app)  # enable CORS

# Function to load Google Gemini Pro Vision API And get response
def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, image[0], prompt])
    return response.text

@app.route("/")
def index():
    return jsonify({"message": "Hello, Welcome to Dr.Ved"})

@app.route("/chat", methods=['POST'])
def chat():
    # Implement your chat functionality here
    pass

@app.route("/instadoc", methods=['POST'])
def instadoc():
    # Implement your instadoc functionality here
    pass

@app.route("/report", methods=['POST'])
def report():
    # Implement your report functionality here
    pass

@app.route("/upload", methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({"message": "File uploaded successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=8080)

