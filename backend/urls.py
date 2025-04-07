from django.urls import path
from .views import soildata, users,SubmitLocationView

urlpatterns = [
    path('fetch/', soildata.as_view(), name="fetch"),
    path('user/', users.as_view(), name="user"),
    path('submit-location/',SubmitLocationView.as_view(),name='submit-location')
]
