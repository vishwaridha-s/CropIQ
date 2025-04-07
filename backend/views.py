from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from .serializers import Sensor, Reg
import bcrypt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import ee

class soildata(APIView):
    def get(self, request):
        mongo_data = settings.SETTINGS_VARS["mongo_data"]
        data = list(mongo_data.find({}, {'_id': 0}))
        return Response(data) 

    def post(self, request):
        mongo_data = settings.SETTINGS_VARS["mongo_data"]
        datas = request.data
        serialdata = Sensor(data=datas)
        if serialdata.is_valid():
            temp = serialdata.validated_data.get("temperature")
            moist = serialdata.validated_data.get("moisture")
            mongo_data.insert_one({"temperature": temp, "moisture": moist})
            return Response({"message": "Soil data added successfully!"})
        return Response(serialdata.errors, status=400)


class users(APIView):
    def post(self, request, *args, **kwargs):
        action = request.query_params.get("action")
        if action == "signup":
            return self.signup(request)
        elif action == "login":
            return self.login(request)
        return Response({"error": "Specify a valid action (signup/login)"}, status=400)

    def signup(self, request):
        mongo_users = settings.SETTINGS_VARS["mongo_users"]
        credentials = Reg(data=request.data)
        if credentials.is_valid():
            username = credentials.validated_data["username"]
            password = credentials.validated_data["password"]
            if mongo_users.find_one({"username": username}):
                return Response({"error": "User Already Exists"})
            hashedpw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            mongo_users.insert_one({
                "username": username,
                "password": hashedpw
            })
            return Response({"message": "Signup successful!"})
        return Response(credentials.errors, status=400)

    def login(self, request):
        mongo_users = settings.SETTINGS_VARS["mongo_users"]
        credentials = Reg(data=request.data)
        if not credentials.is_valid():
            return Response({"error": "Invalid input"}, status=400)

        username = credentials.validated_data['username']
        password = credentials.validated_data['password']

        user = mongo_users.find_one({"username": username})
        if user:
            retrivedpassword = user['password']
            if isinstance(retrivedpassword, str):
                retrivedpassword = retrivedpassword.encode('utf-8')
            if bcrypt.checkpw(password.encode('utf-8'), retrivedpassword):
                return Response({"message": "Login successful!"})
        return Response({"error": "Invalid credentials"}, status=400)


# Initialize Earth Engine once
ee.Initialize(project="seventh-acrobat-456105-g8")


# @api_view(['GET'])


class SubmitLocationView(APIView):
    def post(self, request):
        try:
            latitude = float(request.data.get('latitude'))
            longitude = float(request.data.get('longitude'))
            district=request.data.get('district')
            state=request.data.get('state')
            ip=request.data.get('ip')

            print(f"\n📍 Received Coordinates: Latitude = {latitude}, Longitude = {longitude}")

            analysis_result = analyze_soil(longitude, latitude)

            print("\n🌱 Soil Analysis Result:")
            for key, value in analysis_result.items():
                print(f"{key}: {value}")

            return Response({
                'message': 'Coordinates received and analyzed successfully.',
                'result': analysis_result
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print("❌ Error:", str(e))
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def analyze_soil(longitude, latitude):
    location = ee.Geometry.Point([longitude, latitude])
    buffer = location.buffer(100)

    landcover = ee.ImageCollection('ESA/WorldCover/v100').first().clip(buffer)
    ph_image = ee.Image('OpenLandMap/SOL/SOL_PH-H2O_USDA-4C1A2A_M/v02').select('b0').multiply(0.1).clip(buffer)
    texture_image = ee.Image('OpenLandMap/SOL/SOL_TEXTURE-CLASS_USDA-TT_M/v02').select('b0').clip(buffer)
    oc_image = ee.Image('OpenLandMap/SOL/SOL_ORGANIC-CARBON_USDA-6A1C_M/v02').select('b0').multiply(0.1).clip(buffer)

    crop_mask = landcover.eq(40)
    crop_area = crop_mask.multiply(ee.Image.pixelArea())
    total_crop_area = crop_area.reduceRegion(
        reducer=ee.Reducer.sum(),
        geometry=buffer,
        scale=10,
        maxPixels=1e9
    )

    ph_val = ph_image.reduceRegion(ee.Reducer.mean(), buffer, 250).get('b0')
    tex_val = texture_image.reduceRegion(ee.Reducer.mode(), buffer, 250).get('b0')
    oc_val = oc_image.reduceRegion(ee.Reducer.mean(), buffer, 250).get('b0')

    districts = ee.FeatureCollection("FAO/GAUL_SIMPLIFIED_500m/2015/level2")
    district = districts.filterBounds(location).first().get('ADM2_NAME')

    result = ee.Dictionary({
        'crop_area_m2': total_crop_area.get('Map'),
        'ph': ph_val,
        'texture_code': tex_val,
        'oc_percent': oc_val,
        'district': district
    }).getInfo()

    texture_classes = {
        1: 'Clay', 2: 'Silty Clay', 3: 'Sandy Clay',
        4: 'Clay Loam', 5: 'Silty Clay Loam', 6: 'Sandy Clay Loam',
        7: 'Loam', 8: 'Silt Loam', 9: 'Silt',
        10: 'Sandy Loam', 11: 'Loamy Sand', 12: 'Sand'
    }

    ph = result['ph']
    oc = result['oc_percent']
    tex_code = result['texture_code']
    area_m2 = result['crop_area_m2']
    district_name = result['district']

    soil_texture = texture_classes.get(int(tex_code), 'Unknown')
    inferred_type = 'Unknown'

    if ph < 5.5 and oc < 1 and tex_code in [11, 12]:
        inferred_type = 'Laterite Soil'
    elif ph < 6.5 and oc < 1.5 and tex_code in [10, 11, 12]:
        inferred_type = 'Red Sandy Soil'
    elif ph >= 7 and oc >= 1.5 and tex_code in [1, 4]:
        inferred_type = 'Black Cotton Soil'
    elif 6.5 <= ph <= 7.5 and 0.5 <= oc <= 2.5 and tex_code in [7, 8, 9]:
        inferred_type = 'Alluvial Soil'
    elif ph > 8.5 and oc < 1:
        inferred_type = 'Saline Soil'
    elif oc > 2.5 and ph < 6:
        inferred_type = 'Peaty Soil'
    elif ph < 6.5 and oc < 1.5 and tex_code in [3, 6, 10]:
        inferred_type = 'Red Soil'
    else:
        inferred_type = f'{soil_texture} (Texture-based type)'

    return {
        'District': district_name,
        'Cropland (m²)': round(area_m2, 2) if area_m2 else 0,
        'Cropland (acres)': round(area_m2 * 0.000247105, 2) if area_m2 else 0,
        'Soil pH': round(ph, 2) if ph else 'N/A',
        'Organic Carbon (%)': round(oc, 2) if oc else 'N/A',
        'Soil Texture': soil_texture,
        'Fertility Estimate (NPK, kg/ha)': round(oc * 10, 2) if oc else 'N/A',
        'Inferred Soil Type': inferred_type
    }
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix
from catboost import CatBoostClassifier
from sklearn.naive_bayes import GaussianNB
import matplotlib.pyplot as plt
import seaborn as sns
# Load dataset
crop_df = pd.read_csv("Crop_recommendation.csv")  # temp, moisture, ph, crop

# Encode target
le = LabelEncoder()
crop_df['crop_encoded'] = le.fit_transform(crop_df['label'])

X = crop_df[['temperature', 'humidity', 'ph']]
y = crop_df['crop_encoded']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Best model: CatBoostClassifier
catboost = CatBoostClassifier(verbose=0)
catboost.fit(X_train, y_train)
y_pred = catboost.predict(X_test)

# Baseline model
baseline = GaussianNB()
baseline.fit(X_train, y_train)
base_pred = baseline.predict(X_test)
acc_cat = accuracy_score(y_test, y_pred)
acc_base = accuracy_score(y_test, base_pred)

plt.bar(["CatBoost", "GaussianNB"], [acc_cat*100, acc_base*100], color=['green', 'red'])
plt.title("Model Accuracy Comparison")
plt.ylabel("Accuracy (%)")
plt.show()
params = {
    'depth': [6, 8],
    'learning_rate': [0.05, 0.1],
    'iterations': [200, 300]
}
grid = GridSearchCV(CatBoostClassifier(verbose=0), params, cv=3, scoring='accuracy')
grid.fit(X_train, y_train)
catboost_best = grid.best_estimator_
def predict_top5_crops(temp, moisture, ph, model, encoder):
    input_df = pd.DataFrame([[temp, moisture, ph]], columns=['temp', 'moisture', 'ph'])
    probs = model.predict_proba(input_df)[0]
    top5_idx = np.argsort(probs)[::-1][:5]
    return encoder.inverse_transform(top5_idx)
rice_df = pd.read_csv("RICE_TNAU_STXT.csv")

def suggest_rice_varieties(district, month_str, soil_texture):
    """
    Suggests rice varieties based on district, full month name, and soil texture.

    Args:
        district (str): District name.
        month_str (str): Full month name (e.g., 'July').
        soil_texture (str): Soil texture.

    Returns:
        list: List of matching rice varieties.
    """
    # Normalize input format
    month_str = month_str.strip().lower().capitalize()
    district = district.strip().lower()
    soil_texture = soil_texture.strip().lower()

    # Normalize columns in the dataset
    rice_df['TNDST'] = rice_df['TNDST'].str.strip().str.lower()
    rice_df['STMT'] = rice_df['STMT'].str.strip().str.lower().str.capitalize()
    rice_df['EDMT'] = rice_df['EDMT'].str.strip().str.lower().str.capitalize()
    rice_df['STXT'] = rice_df['STXT'].str.strip().str.lower()

    # Filter dataset based on input
    filtered_df = rice_df[
        (rice_df['TNDST'] == district) &
        (rice_df['STXT'] == soil_texture) &
        (rice_df['STMT'] <= month_str) &
        (rice_df['EDMT'] >= month_str)
    ]

    return filtered_df['VRTS'].unique()
def final_prediction(temp, moisture, ph, district, month, soil_texture):
    """
    Predicts top 5 crops with confidence and suggests rice varieties if rice is among them.
    """
    # Get top 5 predictions with confidence
    top_crops = predict_top5_crops(temp, moisture, ph, catboost, le)
    print("🌿 Top 5 Crop Predictions with Confidence:")
    for crop, confidence in top_crops:
        print(f" - {crop}: {confidence:.2f}%")

    # Check if rice is among the predictions
    crop_names = [crop.lower() for crop, _ in top_crops]
    if "rice" in crop_names:
        print("\n🌾 Since 'Rice' is among top crops, suggesting suitable rice varieties...")

        varieties = suggest_rice_varieties(district, month, soil_texture)

        if len(varieties) == 0:
            print("❗ No matching rice varieties found for the given configuration.")
        else:
            print("✅ Recommended Rice Varieties:")
            for v in varieties:
                print(" -", v)

    else:
        print("\n🌽 'Rice' not in top 5 suggestions. Try growing another from above.")
def predict_top5_crops(temp, moisture, ph, model, label_encoder):
    """
    Predicts the top 5 crop suggestions with their confidence scores.

    Returns:
        List of tuples: (Crop, Confidence %)
    """
    # Changed 'moisture' to 'humidity' in columns
    input_data = pd.DataFrame([[temp, moisture, ph]], columns=['temperature', 'humidity', 'ph'])
    proba = model.predict_proba(input_data)[0]  # Get probability for each class
    crop_classes = label_encoder.inverse_transform(np.arange(len(proba)))

    crop_confidence = list(zip(crop_classes, proba * 100))
    top5 = sorted(crop_confidence, key=lambda x: x[1], reverse=True)[:5]

    return top5  # List of (crop, probability %) tuples
final_prediction(
    temp=20.87,
    moisture=82.00,
    ph=6.5,
    district="Kanchipuram",
    month="august",
    soil_texture="Loamy sand"
)
