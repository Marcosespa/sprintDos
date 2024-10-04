from django.urls import path
from . import views

urlpatterns = [
    path('', views.cronograma_index, name='cronograma_index'),
]
