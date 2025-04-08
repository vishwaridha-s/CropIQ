from django.urls import path
from .views import *

urlpatterns = [
    path('fetch/', soildata.as_view(), name="fetch"),
    path('user/', users.as_view(), name="user"),
    path('submit-location/',SubmitLocationView.as_view(),name='submit-location'),
    path('predict-crop/', PredictCropView.as_view(), name='predict-crop'),
]
