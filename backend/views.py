from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from .serializers import Sensor, Reg
import bcrypt

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
