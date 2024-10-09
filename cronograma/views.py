from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect, render
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

@login_required
def agregar_pago(request, cronograma_id):
    cronograma = get_object_or_404(Cronograma, id=cronograma_id)

    if request.method == 'POST':
        fecha_pago = request.POST.get('fecha_pago')
        valor_pago = request.POST.get('valor_pago')
        estado_pago = request.POST.get('estado_pago')
        tipo_pago = request.POST.get('tipo_pago')
        nombre_pago = request.POST.get('nombre_pago')

        pago = Pago.objects.create(
            cronograma=cronograma,
            usuario_padre=request.user,
            fecha_pago=fecha_pago,
            valor_pago=valor_pago,
            estado_pago=estado_pago,
            tipo_pago=tipo_pago,
            nombre_pago=nombre_pago
        )

        messages.success(request, 'Pago agregado exitosamente.')
        return redirect('cronograma_index') 

    return render(request, 'agregar_pago.html', {'cronograma': cronograma})