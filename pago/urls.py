from django.urls import path
from . import views

urlpatterns = [
    path('procesar/', views.procesar_pago, name='procesar_pago'),
    path('pendiente/', views.pago_pendiente, name='pago_pendiente'),
]