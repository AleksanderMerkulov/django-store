from django.contrib import admin
from django.urls import path, include

from logic.views import mainPage, RegisterUser, LoginUser

urlpatterns = [
    path('',  mainPage),
    path('logup/', RegisterUser.as_view(), name='logup'),
    path('login/', LoginUser.as_view(), name='login'),

]