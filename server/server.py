from flask import Flask, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return jsonify({"message": "Hello, Welcome to Dr.Ved"})


@app.route("/chat")
def chat():
    return jsonify({"message": "Hello World, this is a chatbot"})
    


@app.route("/instadoc")
def instadoc():
    return jsonify({"message": "Hello World, this is an instadoc bot"})

@app.route("/report")
def report():
    return jsonify({"message": "Hello World, this is a report bot"})

if __name__ == "__main__":
    app.run(debug=True, port=8080)