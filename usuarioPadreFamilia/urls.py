from django.urls import path, include
from . import views
from .views import index_PadreFamilia  # Importar la vista desde views.py


urlpatterns = [
    path('index_PadreFamilia/', index_PadreFamilia, name='index_PadreFamilia'),  # Ruta dentro de 'usuarioPadreFamilia'
   path('salir/', views.salir, name="salir"),
    path('cronograma_index/', views.cronograma, name='cronograma_index'),
    path('health/', views.health_check, name='health'),
    path('procesar_pago/', views.pago, name='procesar_pago'),
    path('realizar_pago/', views.realizarpago, name='realizar_pago'),
    path('pagos/', views.pagos_filtrados, name='pagos_filtrados'),
    path('salir/', views.salir, name='salir'),
    path('cronograma/', include('cronograma.urls')),
]

