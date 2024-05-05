from django.contrib import admin
from django.urls import path, include

from logic.views import *

urlpatterns = [
    path('',  mainPage, name='home'),
    path('logup/', RegisterUser.as_view(), name='logup'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutUser.as_view(), name='logout'),
    path('accounts/profile/', profile, name='profile'),
    path('edit_profile/', change_profile, name='change_profile'),
    path('logs/', show_logs, name='logs'),
    path('otchet/', otchet, name='otchet'),
    path('order/<int:pk>', chek, name='order'),
    path('product/<int:pk>', show_curr_tovar, name='show_curr_tovar'),
    path('buy/<int:pk>', buy_curr_tovar, name='buy_curr_tovar'),

]
