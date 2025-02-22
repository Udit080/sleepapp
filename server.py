import pandas as pd
import numpy as np
from flask import Flask, request, jsonify
import pickle
import requests

app = Flask(__name__)

# Load the model
try:
    with open("models/lgbm_model.pkl", "rb") as f:
        model = pickle.load(f)
    print("Model loaded successfully!")
except Exception as e:
    print("Error loading model:", e)

# Set up Hugging Face API key
HUGGING_FACE_API_KEY = "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"  # Replace with your Hugging Face API key
HUGGING_FACE_API_URL = "https://huggingface.co/HuggingFaceH4/zephyr-7b-beta"  # Replace with your model endpoint

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        print("Received data:", data)  # Debugging
        
        # Convert JSON input to DataFrame
        input_data = pd.DataFrame([data])

        input_data = input_data.astype({
            "gender": int,
            "occupation": int,
            "sleepDuration": int,
            "sleepQuality": int,
            "physicalActivity": int,
            "stressLevel": int,
            "bmiCategory": int,
            "heartRate": int,
            "dailySteps": int,
            "age": int,
            "bloodPressure": int
        })

        print("Formatted input data:", input_data)  # Debugging

        # Get class probabilities
        probabilities = model.predict(input_data)

        # Handle multi-class output
        if isinstance(probabilities, np.ndarray) and len(probabilities.shape) > 1:
            predicted_class = int(np.argmax(probabilities, axis=1)[0])
            probability_list = probabilities[0].tolist()  # Convert to Python list
        else:
            predicted_class = int(probabilities[0] > 0.5)  # For binary classification
            probability_list = [1 - probabilities[0], probabilities[0]]

        print("Predicted class:", predicted_class)
        print("Class probabilities:", probability_list)

        return jsonify({
            "prediction": predicted_class,
            "probabilities": probability_list
        })
    except Exception as e:
        print("Prediction error:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json.get("message")
        print("User  message:", user_message)  # Debugging

        # Call Hugging Face API to get a response
        headers = {
            "Authorization": f"Bearer {HUGGING_FACE_API_KEY}"
        }
        payload = {
            "inputs": user_message,
        }

        response = requests.post(HUGGING_FACE_API_URL, headers=headers, json=payload)
        response_data = response.json()

        if response.status_code == 200:
            bot_message = response_data[0]['generated_text']  # Adjust based on the model's response format
        else:
            bot_message = "Sorry, I couldn't process your request."

        print("Bot response:", bot_message)  # Debugging

        return jsonify({"response": bot_message})
    except Exception as e:
        print("Chat error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    from waitress import serve
    print("🚀 Starting production server...")
    serve(app, host="0.0.0.0", port=5001)