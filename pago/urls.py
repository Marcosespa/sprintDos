from django.urls import path
from . import views

urlpatterns = [
    path('procesar_pago/', views.procesar_pago, name='pago_procesar_pago'),
    path('gerente/pagosPendientes/', views.pago_pendiente, name='pago_pendiente'),
]
