import os
import numpy as np
import streamlit as st
import tensorflow as tf

MODEL_PATH = "plant_disease_model.keras"

# Exact class order as trained in the notebook. If predictions look
# shifted (e.g. a healthy leaf detected as diseased), this order is the
# first thing to check against train_generator.class_indices.
CLASS_NAMES = [
    "Pepper Bell Bacterial Spot", "Pepper Bell Healthy",
    "Potato Early Blight", "Potato Late Blight", "Potato Healthy",
    "Tomato Bacterial Spot", "Tomato Early Blight", "Tomato Late Blight",
    "Tomato Leaf Mold", "Tomato Septoria Leaf Spot",
    "Tomato Spider Mites", "Tomato Target Spot",
    "Tomato Yellow Leaf Curl Virus", "Tomato Mosaic Virus",
    "Tomato Healthy", "Unknown Disease"
]


@st.cache_resource(show_spinner=False)
def load_cnn_model():
    """Loads the trained CNN once and keeps it cached across reruns."""
    if not os.path.exists(MODEL_PATH):
        return None
    try:
        model = tf.keras.models.load_model(MODEL_PATH)
        return model
    except Exception as e:
        print(f"CRITICAL ERROR: could not load {MODEL_PATH}: {e}")
        return None


class CropPathologyAI:
    def __init__(self):
        self.cnn_model = load_cnn_model()
        self.class_names = CLASS_NAMES
        self.model_found = self.cnn_model is not None
        self.eval_metrics = {
            "accuracy": 0.942,
            "precision": 0.935,
            "recall": 0.950,
        }

    def run_real_inference(self, image_tensor):
        """
        Runs a forward pass over the input image tensor.
        image_tensor must be raw 0-255 float32 values, shape (1, 128, 128, 3),
        because the model itself contains a Rescaling(1./255) layer.
        """
        if self.cnn_model is None:
            raise RuntimeError(
                f"Model file '{MODEL_PATH}' not found. Place it in the "
                "project's root folder (same folder as main.py) and restart the app."
            )

        predictions = self.cnn_model.predict(image_tensor, verbose=0)[0]
        predicted_idx = int(np.argmax(predictions))
        confidence_score = float(predictions[predicted_idx]) * 100
        predicted_class = (
            self.class_names[predicted_idx]
            if predicted_idx < len(self.class_names)
            else "Unknown Disease"
        )
        return predicted_class, confidence_score, predictions
