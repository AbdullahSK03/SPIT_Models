from flask import Flask, request, jsonify
from joblib import load

app = Flask(__name__)

# Load the model
model = load('model.joblib')

@app.route('/', methods=['POST', 'GET'])
def predict():
    # Get the data from the POST request.
    data = request.get_json(force=True)

    # Make prediction using the model loaded
    prediction = model.predict([np.array(data['feature'])])

    # Take the first value of prediction
    output = prediction[0]

    return jsonify(output)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
