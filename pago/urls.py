from django.urls import path
from . import views

urlpatterns = [
    path('realizar/', views.realizar_pago, name='realizar_pago'),
    path('procesar/', views.procesar_pago, name='procesar_pago'),
    path('pendiente/', views.pago_pendiente, name='pago_pendiente'),
]