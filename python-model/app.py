
import os

# Force CPU mode before importing TensorFlow
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np

app = Flask(__name__)

# Load model only once
model = load_model("cifar10_model.keras", compile=False)

labels = [
    "airplane",
    "automobile",
    "bird",
    "cat",
    "deer",
    "dog",
    "frog",
    "horse",
    "ship",
    "truck"
]


@app.route("/")
def home():
    return "CIFAR-10 Flask API Running"


@app.route("/predict", methods=["POST"])
def predict():

    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    try:
        file = request.files["image"]

        image = Image.open(file).convert("RGB")
        image = image.resize((32, 32))

        img = np.array(image, dtype=np.float32) / 255.0
        img = np.expand_dims(img, axis=0)

        prediction = model.predict(img, verbose=0)

        index = int(np.argmax(prediction))
        confidence = float(np.max(prediction)) * 100

        return jsonify({
            "class": labels[index],
            "confidence": round(confidence, 2)
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)