from django.contrib import admin
from django.urls import path, include

from logic.views import mainPage, RegisterUser, LoginUser, change_profile, LogoutUser

urlpatterns = [
    path('',  mainPage, name='home'),
    path('logup/', RegisterUser.as_view(), name='logup'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutUser.as_view(), name='logout'),
    path('edit_profile/', change_profile, name='change_profile'),
    path('logs/', change_profile, name='logs'),

]
