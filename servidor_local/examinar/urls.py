from django.contrib import admin
from django.urls import path,include
from .views import listado_view,examinar_registro

urlpatterns = [
    path('', listado_view, name='home'),
    path("<str:archivo>/", examinar_registro),
]