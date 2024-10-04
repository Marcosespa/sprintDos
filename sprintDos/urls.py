from django.contrib import admin
from django.urls import include, path
from pago.views import pagina_principal  # Importa la vista de la página principal

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', pagina_principal, name='pagina_principal'),
    path('usuarioPadreFamilia/', include('usuarioPadreFamilia.urls')),
    path('pago/', include('pago.urls')),
    path('cronograma/', include('cronograma.urls')),
]
