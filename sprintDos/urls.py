from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LogoutView

from . import views
import usuarioPadreFamilia.urls  # Asegúrate de importar las URLs de tu app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('usuarioPadreFamilia/', include('usuarioPadreFamilia.urls')),
    path('crear-usuario/', views.crear_usuario, name='crear_usuario'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('health/', views.health_check, name='health'),
    path(r'', include('social_django.urls')),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('pago/', include('pago.urls')),
    path('cronograma/', include('cronograma.urls')),
]
