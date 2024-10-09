from django.urls import path
from . import views

urlpatterns = [
    #path('', views.cronograma_index, name='cronograma_index'),
    path('cronograma_list/', views.cronograma_list, name='cronograma_list'),
    path('pagos/', views.pagos_filtrados, name='pagos_filtrados'),

]
