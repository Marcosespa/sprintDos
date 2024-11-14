from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LogoutView

from pago.views import procesar_pago
from . import views
import usuarioPadreFamilia.urls  # Asegúrate de importar las URLs de tu app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # Página principal para el index
    path('usuarioPadreFamilia/', include('usuarioPadreFamilia.urls')),
    path('crear-usuario/', views.crear_usuario, name='crear_usuario'),
    path('cronograma_index/', views.cronograma, name='cronograma_index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('health/', views.health_check, name='health'),
    path('procesar_pago/', procesar_pago, name='procesar_pago'), 
    path(r'', include('django.contrib.auth.urls')),
    path(r'', include('social_django.urls')),
    path('logout/', LogoutView.as_view(), name='logout'),

]
