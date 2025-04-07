from rest_framework import serializers
from .models import soil
class Sensor(serializers.ModelSerializer):
    class Meta:
        model=soil
        fields="__all__"
    # temperature = serializers.FloatField()
    # moisture = serializers.FloatField()
from django.contrib.auth.models import User
class Reg(serializers.ModelSerializer):
     class Meta:
        model=User
        fields="__all__"
    # username = serializers.CharField(max_length=150)
    # password = serializers.CharField(write_only=True)
    # 
