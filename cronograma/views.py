from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages  
from .forms import PagoForm  
from usuarioPadreFamilia.models import UsuarioPadreFamilia
from cronograma.models import Cronograma
from pago.models import Pago
from django.views.decorators.csrf import csrf_exempt

# Vista de índice de cronograma
@login_required
def cronograma_index(request):
    usuario = request.user  # This is already a UsuarioPadreFamilia instance
    cronogramas = Cronograma.objects.filter(usuario_padre=usuario)
    cronograma_list = []
    for cronograma in cronogramas:
        pagos = Pago.objects.filter(cronograma=cronograma, usuario_padre=usuario)
        cronograma_list.append({
            'cronograma': cronograma,
            'pagos': pagos
        })

    return render(request, 'cronograma_index.html', {'cronograma_list': cronograma_list})

# Vista para agregar un nuevo pago
@login_required
@csrf_exempt
def agregar_pago(request, cronograma_id):
    cronograma = get_object_or_404(Cronograma, id=cronograma_id)

   
    if request.method == 'POST':
        form = PagoForm(request.POST)  
        if form.is_valid():
            pago = form.save(commit=False)
            pago.cronograma = cronograma
            pago.usuario_padre = request.user
            pago.save()  # Guardar el pago

            messages.success(request, 'Pago agregado exitosamente.')
            return redirect('cronograma_index')
    else:
       
        form = PagoForm()

    
    return render(request, 'agregar_pago.html', {'form': form, 'cronograma': cronograma})