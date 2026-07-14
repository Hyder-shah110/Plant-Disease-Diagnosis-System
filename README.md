# DataZone - Plant Disease Diagnosis Dashboard

## Project Overview

DataZone is a web-based AI project developed for a university semester project. It helps users identify plant diseases by uploading a leaf image. A trained Convolutional Neural Network (CNN) analyzes the image and returns the predicted disease, a confidence score, and a treatment plan.

Built using Python, Streamlit, and TensorFlow/Keras.

## Main Features

### Leaf Image Scanner
Users upload a plant leaf image directly into the system.

Supported formats: JPG, JPEG, PNG, WEBP, TIFF, JFIF

### Real CNN Disease Detection
The uploaded image is resized to 128x128 and passed through a trained CNN
(`plant_disease_model.keras`), which classifies it into one of 16 categories
covering Pepper Bell, Potato, and Tomato crops (both healthy and diseased states).

The dashboard shows:
- Detected crop and disease
- Real model confidence score
- Top-5 prediction breakdown chart (from the model's actual softmax output)

### Treatment Recommendation System
Based on the detected disease, the system shows:
- Likely pathogen
- A prescribed treatment plan (biological/chemical control steps)
- Action priority (e.g. Critical Alert, Medium Priority, No Action Needed)

Treatment reference data lives in `disease_info.py` and covers all 16 trained classes.

### AI Expert Insights (Groq)
After a detection, the app sends the predicted disease and confidence to Groq's
`llama-3.3-70b-versatile` model, which generates a plain-language clinical summary
and management plan. This is text-based reasoning grounded in the real CNN result,
not independent image analysis.

### Session Analytics Dashboard
Every image you analyze during a session is logged. Charts show:
- Detections per crop (bar chart)
- Detection share by crop (pie chart)
- Model confidence trend across your session (line chart)

These charts reflect real detections you've made, not simulated data.

### Explainable AI Report
For each detection, a horizontal bar chart shows the model's top candidate classes
and their real probabilities, plus a plain-language summary of what the confidence
score means.

## Project Structure

```
PlantDiseaseProject/
├── main.py                  # Streamlit app, UI, and tab layout
├── model.py                 # Loads the CNN and runs real inference
├── preprocessing.py         # Resizes/prepares leaf images for the model
├── visualization.py         # Plotly charts for the analytics dashboard
├── explanation.py           # Prediction breakdown chart + plain-language summary
├── disease_info.py          # Pathogen/treatment reference data (16 classes)
├── requirements.txt         # Python dependencies
├── plant_disease_model.keras  # Trained CNN (you provide this)
├── .streamlit/
│   └── secrets.toml          # Groq API key (not committed to git)
└── README.md
```

## Setup Instructions

1. Place `plant_disease_model.keras` in the project root (same folder as `main.py`).
2. Create a `.streamlit` folder in the project root, and inside it a `secrets.toml`
   file containing:
   ```
   GROQ_API_KEY = "your-groq-key-here"
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the app:
   ```
   streamlit run main.py
   ```
5. The app opens in your browser, usually at `http://localhost:8501`.

## Supported Classes

Pepper Bell Bacterial Spot, Pepper Bell Healthy, Potato Early Blight, Potato Late
Blight, Potato Healthy, Tomato Bacterial Spot, Tomato Early Blight, Tomato Late
Blight, Tomato Leaf Mold, Tomato Septoria Leaf Spot, Tomato Spider Mites, Tomato
Target Spot, Tomato Yellow Leaf Curl Virus, Tomato Mosaic Virus, Tomato Healthy,
Unknown Disease.

If detections seem shifted (e.g. a healthy leaf detected as diseased), check that
the class order in `model.py` (`CLASS_NAMES`) matches the order used during
training (`train_generator.class_indices` in the training notebook).

## Technology Stack

- **Frontend:** Streamlit, custom CSS
- **Backend / ML:** Python, TensorFlow/Keras, NumPy
- **Image Processing:** Pillow (PIL)
- **Data Visualization:** Plotly, NetworkX
- **AI Insights:** Groq API (llama-3.3-70b-versatile)

## Notes

- Model predictions are decision-support, not a certified diagnosis. For critical
  crop decisions, confirm with a local agricultural expert.
- Never commit `.streamlit/secrets.toml` to version control - add it to `.gitignore`.
