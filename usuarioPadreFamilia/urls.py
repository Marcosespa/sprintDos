from django.urls import path
from . import views
from .views import index_PadreFamilia  # Importar la vista desde views.py

urlpatterns = [
    path('index/', views.index_PadreFamilia, name='index_PadreFamilia'),  # Ruta dentro de 'usuarioPadreFamilia'

]



