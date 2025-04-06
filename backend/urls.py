from django.urls import path
from .views import soildata, users

urlpatterns = [
    path('fetch/', soildata.as_view(), name="fetch"),
    path('user/', users.as_view(), name="user"),
]
