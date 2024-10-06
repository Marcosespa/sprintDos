from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.views.generic.edit import UpdateView
from usuarioPadreFamilia.models import UsuarioPadreFamilia
from cronograma.models import Cronograma
from django.shortcuts import render, get_object_or_404


class SimpleLoginView(LoginView):
    template_name = 'app/login.html'
    redirect_authenticated_user = True

@login_required  
def usuario_padre_familia_edit_view(request):
    usuario = UsuarioPadreFamilia.objects.first()  
    if request.method == 'POST':
        form = UsuarioPadreFamilia(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('edit_usuario') 
    else:
        form = UsuarioPadreFamilia(instance=usuario)
    return render(request, 'app/usuario_edit.html', {'form': form})
def index(request):
    return render(request, 'usuarioPadreFamilia/index.html')  


def index_PadreFamilia(request):
    # Lógica de la vista
    return render(request, 'index_PadreFamilia.html')

def pagos_por_cronograma(request, cronograma_id):
    cronograma = get_object_or_404(Cronograma, id=cronograma_id)
    pagos = cronograma.pago_set.all()  # Obtener todos los pagos asociados al cronograma
    return render(request, 'pagos_por_cronograma.html', {'cronograma': cronograma, 'pagos': pagos})