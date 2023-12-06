from django.contrib import admin
from django.urls import path,include
from .views import listado_view

urlpatterns = [
    path('', listado_view)
]