from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='usuarioPadreFamilia_index'),  # Página principal
]
