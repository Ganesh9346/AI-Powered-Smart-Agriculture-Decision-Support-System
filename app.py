import gradio as gr
import numpy as np
import pickle
import json
from tensorflow.keras.models import load_model
from PIL import Image


import gradio as gr
import numpy as np
import pickle
import json
from tensorflow.keras.models import load_model
from PIL import Image

# LOAD MODELS

ann_model = load_model("crop_ann_model.keras")

with open("label_encoder.pkl", "rb") as f:
    crop_le = pickle.load(f)

leaf_model = load_model("leaf_disease_cnn_model.keras")

with open("leaf_classes.json", "r") as f:
    leaf_classes = json.load(f)



index_to_class = {v: k for k, v in leaf_classes.items()}


# DISEASE SUGGESTIONS

disease_suggestions = {
    "Tomato_Late_blight": "Apply metalaxyl fungicide and avoid overhead watering.",
    "Tomato_Early_blight": "Use chlorothalonil spray and remove infected leaves.",
    "Tomato_Leaf_Mold": "Reduce humidity and apply copper fungicide.",
    "Tomato_Bacterial_spot": "Apply copper-based bactericide and avoid leaf wetness.",

    "Potato_Late_blight": "Spray systemic fungicide and destroy infected plants.",
    "Potato_Early_blight": "Apply mancozeb fungicide every 7 days.",

    "Apple_Apple_scab": "Spray captan fungicide and remove fallen leaves.",
    "Apple_Black_rot": "Prune infected branches and apply copper spray.",

    "Corn_Common_rust": "Use resistant hybrids and apply fungicide if severe.",
    "Corn_Cercospora_leaf_spot Gray_leaf_spot": "Apply azoxystrobin fungicide.",

    "Pepper__bell___Bacterial_spot": "Apply copper-based bactericide and improve air circulation."
}


# FUNCTIONS

def predict_disease(img):
    img = img.resize((128,128))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = leaf_model.predict(img_array)[0]
    sorted_indices = np.argsort(prediction)[::-1]

    for idx in sorted_indices:
        disease_name = index_to_class[idx]
        if disease_name != "PlantVillage":
            confidence = prediction[idx] * 100

            suggestion = disease_suggestions.get(
                disease_name,
                "Remove infected leaves, apply suitable fungicide, and monitor regularly."
            )

            return f"""🌿 **Disease:** {disease_name}
📊 **Confidence:** {confidence:.2f}%

💡 **Suggestion:**
{suggestion}"""

def predict_crop(N, P, K, temperature, humidity, ph, rainfall):
    sample = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
    prediction = ann_model.predict(sample)
    predicted_class = np.argmax(prediction, axis=1)
    crop_name = crop_le.inverse_transform(predicted_class)
    return f"🌾 **Recommended Crop:** {crop_name[0]}\n\n✅ **Perfect match for your soil & climate conditions!**"

def calculate_profit(acres, yield_per_acre, price_per_kg, total_cost):
    if acres and yield_per_acre and price_per_kg and total_cost:
        total_yield = acres * yield_per_acre
        total_revenue = total_yield * price_per_kg
        profit = total_revenue - total_cost
        profit_margin = (profit / total_revenue) * 100 if total_revenue > 0 else 0

        return f"""💰 **Profit Analysis**

📏 **Land Size:** {acres} acres
🌾 **Total Yield:** {total_yield:,.0f} kg
💵 **Total Revenue:** ₹{total_revenue:,.0f}
💸 **Total Cost:** ₹{total_cost:,.0f}
💚 **Net Profit:** ₹{profit:,.0f}
📈 **Profit Margin:** {profit_margin:.1f}%"""
    return "⚠️ Please fill all fields to calculate profit!"


# ENHANCED CUSTOM CSS

custom_css = """
body {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

h1 {
    text-align: center;
    color: #ffffff;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    font-size: 2.5em;
    margin-bottom: 10px;
}

.gr-markdown h1 {
    color: #ffffff !important;
}

.gr-tab {
    background: linear-gradient(45deg, #4CAF50, #45a049) !important;
    border-radius: 15px !important;
    margin: 5px !important;
    font-weight: bold !important;
    color: white !important;
    border: none !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
}

.gr-tab-active {
    background: linear-gradient(45deg, #2E7D32, #1B5E20) !important;
    transform: translateY(-2px) !important;
}

.gr-button {
    background: linear-gradient(45deg, #FF6B6B, #FF8E8E) !important;
    color: white !important;
    font-weight: bold !important;
    border-radius: 25px !important;
    border: none !important;
    padding: 12px 30px !important;
    font-size: 16px !important;
    box-shadow: 0 6px 20px rgba(255,107,107,0.4) !important;
    transition: all 0.3s ease !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
}

.gr-button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 25px rgba(255,107,107,0.6) !important;
}

.gr-number input, .gr-textbox input {
    border-radius: 15px !important;
    border: 2px solid #4CAF50 !important;
    padding: 12px !important;
    font-size: 16px !important;
    background: rgba(255,255,255,0.95) !important;
    box-shadow: inset 0 2px 5px rgba(0,0,0,0.1) !important;
}

.gr-image {
    border-radius: 20px !important;
    border: 4px solid #4CAF50 !important;
    box-shadow: 0 8px 25px rgba(0,0,0,0.2) !important;
}

.gr-textbox {
    background: linear-gradient(145deg, #ffffff, #f0f8ff) !important;
    border-radius: 20px !important;
    border: 3px solid #4CAF50 !important;
    padding: 20px !important;
    font-size: 16px !important;
    box-shadow: 0 8px 25px rgba(76,175,80,0.3) !important;
    line-height: 1.6 !important;
}

.gr-group {
    background: rgba(255,255,255,0.95) !important;
    border-radius: 25px !important;
    padding: 30px !important;
    box-shadow: 0 15px 35px rgba(0,0,0,0.1) !important;
    border: 1px solid rgba(76,175,80,0.3) !important;
    backdrop-filter: blur(10px) !important;
}

.animated-icon {
    font-size: 3em;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
}

.header-glow {
    box-shadow: 0 0 30px rgba(76,175,80,0.6);
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 20px;
}
"""


# ENHANCED GRADIO UI

with gr.Blocks(css=custom_css, theme=gr.themes.Soft()) as app:

    # Header Section
    gr.HTML("""
    <div style='text-align: center; padding: 30px; background: linear-gradient(45deg, rgba(76,175,80,0.9), rgba(46,125,50,0.9)); border-radius: 25px; margin: 20px; box-shadow: 0 15px 40px rgba(0,0,0,0.2);'>
        <div class='animated-icon'>🌱</div>
        <h1>Smart Agriculture AI System</h1>
        <p style='color: #ffffff; font-size: 1.2em; margin: 10px 0;'>🚀 Crop Recommendation | 🌿 Leaf Disease Detection | 💰 Profit Calculator</p>
        <div style='font-size: 1.1em; color: #e8f5e8;'>
            Powered by Deep Learning Models • Instant Analysis • Farmer Friendly
        </div>
    </div>
    """)

    gr.Markdown("## ✨ Choose Your Tool Below")

    with gr.Tabs():
        # Crop Recommendation Tab
        with gr.TabItem("🌾 Crop Recommendation", elem_id="crop-tab"):
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### 📊 Enter Soil & Climate Data")
                    gr.Markdown("*Get the perfect crop for your conditions*")

                with gr.Column(scale=1):
                    gr.Markdown("![crop](https://images.unsplash.com/photo-1611100481087-2eb83c6dd97c?w=300)")

            with gr.Group():
                with gr.Row():
                    with gr.Column():
                        N = gr.Number(label="🌱 Nitrogen (N) ppm", value=50, precision=0)
                        P = gr.Number(label="💎 Phosphorus (P) ppm", value=30, precision=0)
                        K = gr.Number(label="🔥 Potassium (K) ppm", value=40, precision=0)
                    with gr.Column():
                        temperature = gr.Number(label="🌡️ Temperature (°C)", value=25.0, precision=1)
                        humidity = gr.Number(label="💧 Humidity (%)", value=70.0, precision=1)
                        ph = gr.Number(label="🧪 Soil pH", value=6.5, precision=1)
                        rainfall = gr.Number(label="🌧️ Rainfall (mm)", value=100.0, precision=1)

                crop_output = gr.Textbox(label="🌾 AI Prediction", lines=4, interactive=False)

                gr.Button("🚀 Predict Best Crop", variant="primary", size="lg").click(
                    predict_crop,
                    inputs=[N,P,K,temperature,humidity,ph,rainfall],
                    outputs=crop_output
                )

        # Leaf Disease Detection Tab
        with gr.TabItem("🌿 Leaf Disease Detection", elem_id="disease-tab"):
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### 🔍 Upload Leaf Image")
                    gr.Markdown("*Instant disease detection with treatment suggestions*")

                with gr.Column(scale=1):
                    gr.Markdown("![leaf](https://images.unsplash.com/photo-1589924356081-f203baee95f3?w=300)")

            with gr.Group():
                image_input = gr.Image(type="pil", label="📸 Upload Plant Leaf Image", height=300)
                disease_output = gr.Textbox(label="🔬 Disease Analysis", lines=6, interactive=False)

                gr.Button("🔍 Analyze Disease", variant="primary", size="lg").click(
                    predict_disease,
                    inputs=image_input,
                    outputs=disease_output
                )

        # Profit Calculator Tab
        with gr.TabItem("💰 Profit Calculator", elem_id="profit-tab"):
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### 💵 Smart Profit Calculator")
                    gr.Markdown("*Calculate ROI before planting*")

                with gr.Column(scale=1):
                    gr.Markdown("![profit](https://images.unsplash.com/photo-1558618047-3c8c76fdd7f4?w=300)")

            with gr.Group():
                with gr.Row():
                    with gr.Column():
                        acres = gr.Number(label="📏 Land Size (Acres)", value=1.0, precision=1)
                        yield_per_acre = gr.Number(label="🌾 Yield per Acre (kg)", value=2000, precision=0)
                    with gr.Column():
                        price_per_kg = gr.Number(label="💰 Market Price per kg (₹)", value=25, precision=0)
                        total_cost = gr.Number(label="💸 Total Cost (₹)", value=50000, precision=0)

                profit_output = gr.Textbox(label="💚 Profit Breakdown", lines=8, interactive=False)

                gr.Button("💰 Calculate Profit", variant="primary", size="lg").click(
                    calculate_profit,
                    inputs=[acres, yield_per_acre, price_per_kg, total_cost],
                    outputs=profit_output
                )

    # Footer
    gr.HTML("""
    <div style='text-align: center; padding: 30px; margin-top: 40px; color: #ffffff; background: linear-gradient(45deg, rgba(46,125,50,0.9), rgba(27,94,32,0.9)); border-radius: 25px; margin: 20px;'>
        <div style='font-size: 1.3em; margin-bottom: 10px;'>🌟 Happy Farming! 🌟</div>
        <div>Built with ❤️ for Indian Farmers | AI-Powered Precision Agriculture</div>
    </div>
    """)

app.launch()

