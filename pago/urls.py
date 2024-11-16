from django.urls import path
from . import views
app_name = 'pago'
urlpatterns = [
    path('realizar/', views.realizar_pago, name='realizar_pago'),
    path('procesar/', views.procesar_pago, name='procesar_pago'),
    path('pendiente/', views.pago_pendiente, name='pago_pendiente'),
]