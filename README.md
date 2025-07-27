# 🌾 CropIQ - Smart Crop Recommendation System

CropIQ is a smart agricultural decision-support tool that analyzes soil parameters and environmental data to recommend the most suitable crop varieties for a given location. This system empowers farmers, researchers, and agricultural departments to make data-driven crop choices, improve yield, and promote sustainable farming practices.

---

## 🚀 Features

- 🌱 **Crop Recommendation** based on soil fertility (pH, moisture, NPK levels, etc.)
- 🌦️ **Weather & Soil Data Integration** using real-time and historical sources
- 🧠 **Machine Learning**-based classification using CatBoostClassifier
- 📍 **Location-based Insights** via coordinate input and district mapping
- 🗂️ **Django Backend** with MongoDB for dynamic data storage
- 🛰️ **Google Earth Engine** integration for advanced soil analysis
- 🔐 **User Authentication** (Login/Signup for farmers and scientists)
- 📱 **Frontend Integration** via React Native with Expo Location API

---

## 🧪 Tech Stack

- **Backend**: Django, Djongo (MongoDB)
- **Frontend**: React Native (Expo)
- **Database**: MongoDB
- **ML Model**: CatBoostClassifier
- **Geospatial Analysis**: Google Earth Engine
- **Authentication**: Django's auth system

---

## 📊 Machine Learning Details

- **Model**: CatBoostClassifier
- **Training Data**: District-wise soil data (pH, organic carbon, texture, etc.)
- **Prediction Output**: Most suitable crop variety
- **Evaluation**: Accuracy and domain-specific validation

---

## 🌍 Input Parameters

- Location (via coordinates)
- Soil characteristics:
  - pH
  - Moisture
  - Nitrogen (N)
  - Phosphorus (P)
  - Potassium (K)
- Weather data (temperature, rainfall)

---

## 🧪 API Endpoints (Sample)

| Endpoint                  | Method | Description                           |
|--------------------------|--------|---------------------------------------|
| `/api/login/`            | POST   | User login                            |
| `/api/signup/`           | POST   | New user registration                 |
| `/api/soil/analyze/`     | POST   | Soil parameter analysis               |
| `/api/crop/recommend/`   | POST   | Get recommended crops for location    |

---

## ⚙️ Setup Instructions

1. **Clone the repo:**
   ```bash
   git clone https://github.com/yourusername/cropiq.git

2. **Run the Backend**

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
