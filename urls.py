#from django.contrib import admin
from django.urls import path
from accounts import views
from .views import *
from .  import views

urlpatterns = [
   # path("",views.home, name='home' ),
   path('signup/',views.signup_view,name='signup'),
   path('', views.auth_login_view, name='login'),
   path('logout/',views.auth_logout_view,name='logout'),
   path('my_profile/',views.profile_view,name='my_profile'),
   path('profile/<str:username>/',views.user_profile,name='user_profile'),
   path('edit_profile/',views.edit_profile,name="edit_profile"),
]