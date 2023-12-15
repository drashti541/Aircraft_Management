from django.contrib import admin
from django.urls import path, include

from .views import AircraftViewSet, FlightViewSet
from rest_framework import routers 

router = routers.DefaultRouter()
router.register(r'aircrafts', AircraftViewSet)
router.register(r'flights', FlightViewSet)

urlpatterns = [
    path('',include(router.urls))
]