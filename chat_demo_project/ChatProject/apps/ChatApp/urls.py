from django.urls import path, re_path, include
from rest_framework import routers
from.views import SparkaiAPI
router = routers.DefaultRouter()


urlpatterns = [
    re_path('sparkai', SparkaiAPI.as_view(), name='sparkai'),

]