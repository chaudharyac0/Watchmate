from django.urls import path
from django import views
from rest_framework.authtoken.views import obtain_auth_token
from user_app.api.views import RegisterView,logout_view


urlpatterns = [
    path('login/',obtain_auth_token,name='login'),
    path('register/',RegisterView,name='register'),
    path('logout/',logout_view,name='logout'),
    
]
