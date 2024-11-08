from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.views.generic.edit import UpdateView
from usuarioPadreFamilia.models import UsuarioPadreFamilia
from django.contrib.auth import logout
from cronograma.models import Cronograma
from django.shortcuts import render, get_object_or_404
from cronograma.models import Cronograma
from pago.models import Pago

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

def health_check(request):
    return JsonResponse({'message': 'OK'}, status=200)


def index_PadreFamilia(request):
    # Lógica de la vista
    cronogramas = Cronograma.objects.all()
    return render(request, 'index_PadreFamilia.html', {'cronogramas': cronogramas})

def salir(request):
    logout(request)  # Esto cierra la sesión del usuario
    return redirect('/')  # Redirige a la página de inicio u otra página

def cronograma(request):
    return render(request, 'cronograma_index.html')

def pago(request):
    return render(request, 'procesar_pago.html')


def pagos_filtrados(request):
    if request.method == "POST":
        # Obtener el ID del cronograma desde el formulario
        cronograma_id = request.POST.get('cronograma_id')

        # Obtener el cronograma específico
        cronograma = get_object_or_404(Cronograma, id=cronograma_id)

        # Filtrar los pagos asociados al cronograma
        pagos = Pago.objects.filter(cronograma=cronograma)

        # Renderizar la vista con los pagos filtrados
        return render(request, 'cronograma.html', {'cronograma': cronograma, 'pagos': pagos})

    # Si es un GET o algo inesperado, redirigir a la página de consulta
    return render(request, 'consulta_cronograma.html')