from django.contrib import admin
from django.urls import path, include

from logic.views import mainPage, RegisterUser, LoginUser, change_profile, LogoutUser, buy_curr_tovar, show_curr_tovar

urlpatterns = [
    path('',  mainPage, name='home'),
    path('logup/', RegisterUser.as_view(), name='logup'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutUser.as_view(), name='logout'),
    path('edit_profile/', change_profile, name='change_profile'),
    path('logs/', change_profile, name='logs'),
    path('product/<int:pk>', show_curr_tovar, name='show_curr_tovar'),
    path('buy/<int:pk>', buy_curr_tovar, name='buy_curr_tovar'),

]
