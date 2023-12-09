from django.contrib import admin
from django.urls import path, include
from forms import views

urlpatterns = [
    path("", views.login, name="login"),
    path("SignPatient", views.signupat, name="signupPatient"),
    path("SignDoctor", views.signupdoc, name="signupDoc"),
    path("home", views.home, name="home"),
    path("index", views.index , name="index"),
    path("logout", views.logout, name="logout"),
]
