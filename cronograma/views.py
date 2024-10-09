from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from usuarioPadreFamilia.models import UsuarioPadreFamilia
from cronograma.models import Cronograma
from pago.models import Pago

# Otras vistas

@login_required
def cronograma_index(request):
    usuario = request.user 
    cronogramas = Cronograma.objects.filter(usuario_padre=usuario)
    cronograma_list = []
    for cronograma in cronogramas:
        pagos = Pago.objects.filter(cronograma=cronograma, usuario_padre=usuario)
        cronograma_list.append({
            'cronograma': cronograma,
            'pagos': pagos
        })

    return render(request, 'cronograma_index.html', {'cronograma_list': cronograma_list})
