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
import datetime
import requests
import traceback
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
            moist = serialdata.validated_data.get("humidity")
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
    mongo_soil = settings.SETTINGS_VARS["mongo_soil"]
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

    mongo_soil.insert_one({"district":district_name,"ph":ph,"texture":soil_texture})

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


class PredictCropView(APIView):
    def get(self, request):
        try:
            # Get latest sensor data from MongoDB
            mongo_data = settings.SETTINGS_VARS["mongo_data"]
            mongo_soil=settings.SETTINGS_VARS["mongo_soil"]
            latest_sensor = mongo_data.find_one(sort=[('_id', -1)])
            latest_data=mongo_soil.find_one(sort=[('_id',-1)])

            # Current month in lowercase
            month = datetime.now().strftime("%B").lower()
            temperature=latest_sensor["temperature"]
            moisture=latest_sensor["moisture"]
            district=latest_data["district"]
            ph=latest_data["ph"]
            texture=latest_data["texture"]
            playload={
                "temperature":temperature,
                "humidity":moisture,
                "ph":ph,
                "district":district,
                "month":month,
                "soil_texture":texture
            }
            response = requests.post(
                "https://c270-35-237-185-90.ngrok-free.app/predict",  # Replace with your actual ngrok URL
                json=playload,
                headers={"Content-Type": "application/json"}
            )

            print("📥 Flask Response Status:", response.status_code)
            print("📥 Flask Response Body:", response.text)

            if response.status_code == 200:
                return Response(response.json())
            else:
                return Response({
                    "error": "Prediction request failed",
                    "status_code": response.status_code,
                    "details": response.text
                }, status=response.status_code)

        except Exception as e:
            print("❌ Exception Occurred:")
            traceback.print_exc()
            return Response({'error': str(e)}, status=500)