from django.urls import path
from .views import index, listado_view, examinar_registro

urlpatterns = [
    path('', index, name='index'),
    path('revisar/', listado_view, name='home'),
    path('revisar/<str:archivo>/', examinar_registro, name='detalle'),
]