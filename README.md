🌱 AI-Powered Smart Agriculture Decision Support System

An intelligent agriculture assistant that helps farmers and researchers with:

✅ Crop Recommendation
✅ Leaf Disease Detection
✅ Profit Analysis

Built using Deep Learning + Gradio + TensorFlow
📌 Features
🌾 Crop Recommendation

Predicts the best crop based on:

Nitrogen (N)

Phosphorus (P)

Potassium (K)

Temperature

Humidity

pH

Rainfall

Uses trained ANN model

🌿 Leaf Disease Detection

Upload plant leaf image

Detects disease using CNN (MobileNetV2)

Provides:

Disease name

Confidence score

Treatment suggestion

💰 Profit Calculator

Calculates:

Total yield

Revenue

Net profit

Profit margin

🧠 Models Used
🔹 Crop Recommendation Model

Algorithm: Artificial Neural Network (ANN)

Input features:

N, P, K, temperature, humidity, pH, rainfall

Output: Best crop label

🔹 Leaf Disease Detection Model

Base model: MobileNetV2 (Transfer Learning)

Image size: 128 × 128

Output: Disease class

🗂️ Project Structure
├── app.py
├── crop_ann_model.keras
├── leaf_disease_cnn_model.keras
├── label_encoder.pkl
├── leaf_classes.json
├── crop_recommendation.csv
├── requirements.txt
└── README.md

⚙️ Installation & Run Locally
1️⃣ Clone the repository
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Run the application
python app.py

🖥️ Tech Stack

Python

TensorFlow / Keras

Scikit-learn

Gradio

NumPy

PIL

📊 Dataset
Crop Recommendation Dataset

Soil nutrients

Weather conditions

Crop labels

Leaf Disease Dataset

PlantVillage dataset

Multiple crop leaf disease classes

🎯 Use Case

This system helps:

👨‍🌾 Farmers → choose best crop & detect diseases
🏫 Students → learn AI in agriculture
🔬 Researchers → build smart farming solutions
🌍 Future Improvements

Fertilizer recommendation

Soil health analysis

Multi-language support

Mobile friendly UI

👨‍💻 Author

Ganesh
AI & Data Science Enthusiast

GitHub:
https://github.com/Ganesh9346

