from django.urls import path
from . import views

urlpatterns = [
    path('index_PadreFamilia/', index_PadreFamilia, name='index_PadreFamilia'),  # Página principal
]



