
import os

# ============================================================
# TensorFlow CPU configuration
# MUST be before importing TensorFlow
# ============================================================

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["TF_NUM_INTRAOP_THREADS"] = "1"
os.environ["TF_NUM_INTEROP_THREADS"] = "1"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
import tensorflow as tf
from PIL import Image
import numpy as np


app = Flask(__name__)


# ============================================================
# Limit TensorFlow CPU threads
# ============================================================

try:
    tf.config.threading.set_intra_op_parallelism_threads(1)
    tf.config.threading.set_inter_op_parallelism_threads(1)
except Exception:
    pass


# ============================================================
# Load CIFAR-10 model
# ============================================================

model = load_model(
    "cifar10_model.keras",
    compile=False
)


# ============================================================
# CIFAR-10 class labels
# ============================================================

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


# ============================================================
# Home endpoint
# ============================================================

@app.route("/")
def home():
    return "CIFAR-10 Flask API Running"


# ============================================================
# Prediction endpoint
# ============================================================

@app.route("/predict", methods=["POST"])
def predict():

    if "image" not in request.files:
        return jsonify({
            "error": "No image uploaded"
        }), 400

    try:

        # Get uploaded image
        file = request.files["image"]

        # Open image
        image = Image.open(file).convert("RGB")

        # CIFAR-10 images are 32x32
        image = image.resize((32, 32))

        # Convert image to NumPy array
        img = np.array(
            image,
            dtype=np.float32
        ) / 255.0

        # Add batch dimension
        img = np.expand_dims(img, axis=0)

        # Direct model inference
        prediction = model(
            img,
            training=False
        ).numpy()

        # Find predicted class
        index = int(np.argmax(prediction))

        # Get confidence
        confidence = float(
            np.max(prediction)
        ) * 100

        result = {
            "class": labels[index],
            "confidence": round(confidence, 2)
        }

        print("Prediction:", result, flush=True)

        return jsonify(result)

    except Exception as e:

        print("Prediction error:", str(e), flush=True)

        return jsonify({
            "error": str(e)
        }), 500


# ============================================================
# Local execution
# ============================================================

if __name__ == "__main__":

    port = int(
        os.environ.get("PORT", 10000)
    )

    app.run(
        host="0.0.0.0",
        port=port
    )

