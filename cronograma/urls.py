from django.urls import path
from . import views

urlpatterns = [
    path('cronograma/', views.cronograma_index, name='cronograma_index'), 
    path('pagos/', views.pagos_filtrados, name='pagos_filtrados'),
    path('health-check/', views.healthCheck, name='health_check'),
    path('cronograma/<int:cronograma_id>/agregar_pago/', views.agregar_pago, name='agregar_pago'),
]