from django.urls import include, path
from rest_framework import routers
from . import views
from GeoSunvey.views import *
urlpatterns = [
    path('login/', views.user_login, name='user_login'),
]

