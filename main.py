import streamlit as st
import pandas as pd
from datetime import datetime

# Page Configuration (must be first Streamlit call)
st.set_page_config(
    page_title="DataZone - AI Plant Pathology Lab",
    layout="wide",
    initial_sidebar_state="expanded"
)

import visualization as vis
import explanation as xai
from disease_info import DISEASE_INFO
from model import CropPathologyAI
from preprocessing import process_uploaded_image

# Custom CSS Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        font-family: 'Poppins', sans-serif;
        background-color: #06040d;
        color: #a584c7;
    }
    .main-title {
        font-size: 34px;
        font-weight: 700;
        color: #00f2fe;
        text-shadow: 0px 0px 15px rgba(0, 242, 254, 0.4);
        margin-bottom: 5px;
    }
    .sub-title {
        font-size: 14px;
        color: #535366;
        margin-bottom: 25px;
    }
    .matrix-card {
        background: rgba(14, 11, 24, 0.95);
        border: 1px solid #1f1b3d;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.7);
    }
    .rep-title {
        font-size: 17px;
        font-weight: 600;
        color: #00f2fe;
        margin-bottom: 12px;
        letter-spacing: 0.5px;
    }
    .treatment-box {
        background: rgba(7, 241, 97, 0.04);
        border: 1px solid rgba(7, 241, 97, 0.2);
        border-radius: 8px;
        padding: 15px;
        margin-top: 15px;
    }
    .rep-text {
        color: #8f8fa3;
        font-size: 14px;
        line-height: 1.6;
    }
    .rep-highlight {
        color: #ff4a5a;
        font-weight: bold;
    }
    [data-testid="stFileUploader"] {
        background: #090614;
        border: 2px dashed #bf7af0;
        border-radius: 10px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Groq client setup - key comes from st.secrets, never hardcoded
groq_client = None
groq_error = None
try:
    from groq import Groq
    api_key = st.secrets.get("GROQ_API_KEY", None)
    if api_key:
        groq_client = Groq(api_key=api_key)
    else:
        groq_error = "No GROQ_API_KEY found in .streamlit/secrets.toml"
except Exception as e:
    groq_error = str(e)

# Session state initialization
if 'ai_core' not in st.session_state:
    st.session_state.ai_core = CropPathologyAI()

if 'detection_history' not in st.session_state:
    st.session_state.detection_history = []

if 'latest_result' not in st.session_state:
    st.session_state.latest_result = None

if 'groq_analysis' not in st.session_state:
    st.session_state.groq_analysis = "Upload an image to trigger real-time AI pathology analysis."

ai_core = st.session_state.ai_core

# Header
st.markdown("<div class='main-title'>DATAZONE: PLANT PATHOLOGY DIGITAL LAB</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>CNN-Based Real-Time Plant Disease Detection</div>", unsafe_allow_html=True)

if not ai_core.model_found:
    st.error(
        "CNN model file 'plant_disease_model.keras' was not found in the project folder. "
        "Place the trained model file in the same directory as main.py, then restart the app. "
        "Detection will not work until the model is present."
    )

tab_dashboard, tab_calibration, tab_reports = st.tabs([
    "Real-Time Detection",
    "Model Info",
    "Explainable AI & Reports"
])

# ==========================================
# TAB 1: Detection Dashboard
# ==========================================
with tab_dashboard:
    st.markdown("<div class='matrix-card'>", unsafe_allow_html=True)
    st.markdown("<div class='rep-title'>UPLOAD PLANT LEAF IMAGE FOR AI ANALYSIS</div>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Choose a leaf image file (JPG, JPEG, PNG, WEBP, TIFF, JFIF)...",
        type=["jpg", "jpeg", "png", "webp", "tiff", "jfif"]
    )

    if uploaded_file is not None:
        col_img1, col_img2 = st.columns([4, 8])
        with col_img1:
            st.image(uploaded_file, caption="Target Crop Specimen", width=280)

        with col_img2:
            with st.spinner("Running CNN inference on the uploaded image..."):
                result = process_uploaded_image(uploaded_file, ai_core)

            if result["success"]:
                st.session_state.latest_result = result
                st.session_state.detection_history.append({
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                    "crop": result["crop"],
                    "disease": result["disease"],
                    "confidence": result["confidence"],
                })

                st.success(f"Detected: **{result['disease']}** ({result['confidence']:.2f}% confidence)")

                if groq_client is not None:
                    with st.spinner("Generating expert explanation via Groq..."):
                        try:
                            disease_data = DISEASE_INFO.get(result["disease"], {})
                            response = groq_client.chat.completions.create(
                                model="llama-3.3-70b-versatile",
                                messages=[
                                    {
                                        "role": "user",
                                        "content": (
                                            f"A CNN plant pathology model analyzed a leaf image and detected "
                                            f"'{result['disease']}' with {result['confidence']:.2f}% confidence. "
                                            f"Likely pathogen: {disease_data.get('pathogen', 'unknown')}. "
                                            "Write a short clinical summary explaining what this means for "
                                            "the plant and a practical management plan, in plain language "
                                            "suitable for a farmer."
                                        )
                                    }
                                ],
                                max_tokens=500
                            )
                            st.session_state.groq_analysis = response.choices[0].message.content
                        except Exception as e:
                            st.session_state.groq_analysis = f"Groq API error: {str(e)}"
                else:
                    st.session_state.groq_analysis = (
                        f"Groq insights unavailable ({groq_error}). "
                        "Detection results above are still from the real CNN model."
                    )
            else:
                st.error(result["message"])

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("### Detection History Analytics")
    history_df = pd.DataFrame(st.session_state.detection_history)

    if history_df.empty:
        st.info("No detections yet. Upload a leaf image above to start building analytics.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<div class='matrix-card'>", unsafe_allow_html=True)
            st.plotly_chart(vis.generate_bar_chart(history_df), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='matrix-card'>", unsafe_allow_html=True)
            st.plotly_chart(vis.generate_pie_chart(history_df), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='matrix-card'>", unsafe_allow_html=True)
            st.plotly_chart(vis.generate_line_chart(history_df), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='matrix-card'>", unsafe_allow_html=True)
            st.plotly_chart(vis.generate_network_topology(), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# TAB 2: Model Info
# ==========================================
with tab_calibration:
    st.markdown("### Model Backend Status")
    st.markdown("<div class='matrix-card'>", unsafe_allow_html=True)
    st.markdown("<div class='rep-title'>CORE MODEL STATUS</div>", unsafe_allow_html=True)

    if ai_core.model_found:
        st.success("CNN model loaded successfully from plant_disease_model.keras")
    else:
        st.error("CNN model not loaded - see error message above.")

    if groq_client is not None:
        st.info("Groq API connected for generating plain-language explanations.")
    else:
        st.warning(f"Groq API not connected: {groq_error}")

    st.write(f"Trained classes: {len(ai_core.class_names)}")
    st.write(", ".join(ai_core.class_names))
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# TAB 3: Explainable AI & Reports
# ==========================================
with tab_reports:
    st.markdown("### AI Pathological & Treatment Report")

    if st.session_state.latest_result is None:
        st.info("Upload and analyze a leaf image in the Detection tab first.")
    else:
        result = st.session_state.latest_result
        disease_info = DISEASE_INFO.get(result["disease"], {})

        st.markdown("<div class='matrix-card'>", unsafe_allow_html=True)
        st.markdown(f"<h2>Diagnosis: <span style='color:#00f2fe;'>{result['disease']}</span></h2>", unsafe_allow_html=True)

        col_r1, col_r2 = st.columns([7, 5])
        with col_r1:
            st.markdown("<div class='rep-title'>CLINICAL PATHOLOGY DIAGNOSIS</div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class='rep-text'>
                * <b>Target Pathogen:</b> <span style='color:#bf7af0; font-weight:600;'>{disease_info.get('pathogen', 'Unknown')}</span><br>
                * <b>Model Confidence:</b> <span class='rep-highlight'>{result['confidence']:.2f}%</span><br>
                * <b>Action Priority:</b> <span style='color:#07F161; font-weight:600;'>{disease_info.get('remediation_speed', 'N/A')}</span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class='treatment-box'>
                <div style='color:#07F161; font-weight:600; font-size:15px; margin-bottom:5px;'>PRESCRIBED TREATMENT PLAN:</div>
                <div class='rep-text' style='color:#e2d9f3; white-space: pre-line;'>{disease_info.get('treatment', 'No data available')}</div>
            </div>
            """, unsafe_allow_html=True)

        with col_r2:
            st.markdown("<div class='rep-title'>PREDICTION BREAKDOWN</div>", unsafe_allow_html=True)
            breakdown_fig = xai.get_prediction_breakdown_plot(
                ai_core.class_names, result["probabilities"]
            )
            st.plotly_chart(breakdown_fig, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='matrix-card'>", unsafe_allow_html=True)
        st.markdown("<div class='rep-title'>PLAIN-LANGUAGE EXPLANATION</div>", unsafe_allow_html=True)
        st.markdown(xai.generate_natural_language_explanation(result["disease"], result["confidence"]))
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='matrix-card'>", unsafe_allow_html=True)
        st.markdown("<div class='rep-title'>AI EXPERT INSIGHTS (GROQ)</div>", unsafe_allow_html=True)
        st.info(st.session_state.groq_analysis)
        st.markdown("</div>", unsafe_allow_html=True)
