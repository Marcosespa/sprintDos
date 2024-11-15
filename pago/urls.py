from django.urls import path
from . import views

urlpatterns = [
    path('procesar_pago/', views.procesar_pago, name='procesar_pago'),
]
