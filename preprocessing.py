import numpy as np
from PIL import Image


def process_uploaded_image(uploaded_file, ai_core_engine):
    """
    Takes an uploaded leaf photo, prepares it for the CNN, and returns
    the real prediction from the model.
    """
    try:
        image = Image.open(uploaded_file).convert('RGB')
        resized_image = image.resize((128, 128))

        # IMPORTANT: the model already has a Rescaling(1./255) layer
        # built in, so we pass raw 0-255 float values here, NOT
        # pre-divided ones. Dividing twice was the earlier bug.
        image_array = np.array(resized_image, dtype=np.float32)
        image_tensor = np.expand_dims(image_array, axis=0)

        disease_result, confidence, full_probabilities = ai_core_engine.run_real_inference(image_tensor)

        detected_crop = "Tomato Crop"
        if "Potato" in disease_result:
            detected_crop = "Potato Crop"
        elif "Pepper" in disease_result:
            detected_crop = "Pepper Bell"

        return {
            "success": True,
            "image": resized_image,
            "disease": disease_result,
            "confidence": confidence,
            "crop": detected_crop,
            "probabilities": full_probabilities,
            "message": "CNN prediction executed successfully.",
        }

    except Exception as error:
        return {
            "success": False,
            "image": None,
            "disease": None,
            "confidence": 0.0,
            "crop": None,
            "probabilities": None,
            "message": f"Error processing image: {str(error)}",
        }
