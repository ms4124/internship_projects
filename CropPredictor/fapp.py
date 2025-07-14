
from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)
# Load model and LabelEncoder
model = joblib.load("model.lb")
le = joblib.load("labelencoder.lb")  # Make sure aapne label encoder bhi save kiya tha

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/calculator.html')
def calculator():
    return render_template('calculator.html')
@app.route('/contact.html')
def contact():
    return render_template('contact.html')
@app.route('/history.html')
def history():
    return render_template('history.html')
@app.route('/predict-farming', methods=['POST'])
def predict_farming():
    try:
        data = request.json
        print("📥 Received JSON:", data)

        features = [
            float(data['N']),
            float(data['P']),
            float(data['K']),
            float(data['temperature']),
            float(data['humidity']),
            float(data['ph']),
            float(data['rainfall'])
        ]

        features_np = np.array([features])
        print("🔍 Features for prediction:", features_np)

        pred_encoded = model.predict(features_np)
        pred_label = le.inverse_transform(pred_encoded)[0]
        print("🌾 Predicted label:", pred_label)
        return jsonify({'predicted_crop': str(pred_label)})
    except Exception as e:
        print("❌ Error in prediction:", str(e))
        return jsonify({'error': 'Error during prediction'}), 500
if __name__ == '__main__':
    app.run(debug=True, port=5001)
