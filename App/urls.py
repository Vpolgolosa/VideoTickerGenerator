from django.urls import path
from . import views

urlpatterns = [
    path('runtext', views.runtext)
]
