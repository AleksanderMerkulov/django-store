from django.contrib import admin
from django.urls import path, include

from logic.views import mainPage

urlpatterns = [
    path('',  mainPage),
]