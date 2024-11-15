from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic.edit import UpdateView
from django.contrib.auth import logout
from usuarioPadreFamilia.models import UsuarioPadreFamilia
from cronograma.models import Cronograma
from pago.models import Pago
from sprintDos.auth0backend import getRole
from django.db.models import Sum
from django.contrib import messages

class SimpleLoginView(LoginView):
    template_name = 'app/login.html'
    redirect_authenticated_user = True

@login_required  
def usuario_padre_familia_edit_view(request):
    role = getRole(request)
    if role == "Gerente":
        usuario = UsuarioPadreFamilia.objects.first()
        if request.method == 'POST':
            form = UsuarioPadreFamilia(request.POST, instance=usuario)
            if form.is_valid():
                form.save()
                return redirect('edit_usuario')
        else:
            form = UsuarioPadreFamilia(instance=usuario)
        return render(request, 'app/usuario_edit.html', {'form': form})
    else:
        return JsonResponse({'message': 'Unauthorized User'}, status=403)

def index(request):
    return render(request, 'usuarioPadreFamilia/index.html')

def health_check(request):
    return JsonResponse({'message': 'OK'}, status=200)

@login_required
def index_PadreFamilia(request):
    try:
        role = getRole(request)
    except (IndexError, AttributeError):
        # If there's no social auth or role, assume a basic authenticated user
        role = "Gerente"
    
    if role == "Padre de Familia" or role == "Gerente":
        try:
            usuario_padre = request.user
            pagos = Pago.objects.filter(usuario_padre=usuario_padre)
            
            # Calculate stats safely
            pagos_pendientes = pagos.filter(estado_pago='PENDIENTE').count()
            total_pagado = pagos.filter(estado_pago='PAGADO').aggregate(Sum('valor_pago'))['valor_pago__sum'] or 0
            
            context = {
                'pagos_pendientes_count': pagos_pendientes,
                'total_pagado': total_pagado,
            }
            return render(request, 'index_PadreFamilia.html', context)
            
        except Exception as e:
            print(f"Error en index_PadreFamilia: {str(e)}")
            context = {
                'pagos_pendientes_count': 0,
                'total_pagado': 0,
            }
            return render(request, 'index_PadreFamilia.html', context)
    else:
        return JsonResponse({'message': 'Unauthorized User'}, status=403)

@login_required
def salir(request):
    logout(request)
    return redirect('https://dev-rgo1o3badtq3r0pa.us.auth0.com/v2/logout?returnTo=http%3A%2F%2F104.198.44.212:8080')

@login_required
def cronograma(request):
    try:
        role = getRole(request)
        if role not in ["Padre de Familia", "Gerente"]:
            messages.error(request, 'Acceso no autorizado.')
            return redirect('index_PadreFamilia')
        return render(request, 'cronograma_index.html')
    except Exception as e:
        messages.error(request, f'Error al acceder al cronograma: {str(e)}')
        return redirect('index_PadreFamilia')

@login_required
def pago(request):
    return render(request, 'procesar_pago.html')

@login_required
def pagos_filtrados(request):
    role = getRole(request)
    if role == "Gerente":
        if request.method == "POST":
            cronograma_id = request.POST.get('cronograma_id')
            cronograma = get_object_or_404(Cronograma, id=cronograma_id)
            pagos = Pago.objects.filter(cronograma=cronograma)
            return render(request, 'cronograma.html', {'cronograma': cronograma, 'pagos': pagos})
        else:
            return render(request, 'consulta_cronograma.html')
    else:
        return JsonResponse({'message': 'Unauthorized User'}, status=403)

@login_required
def dashboard_stats(request):
    user = request.user
    pagos = Pago.objects.filter(usuario_padre=user)
    
    stats = {
        'pagos_pendientes_count': pagos.filter(estado_pago='PENDIENTE').count(),
        'total_pagado': pagos.filter(estado_pago='PAGADO').aggregate(Sum('valor_pago'))['valor_pago__sum'] or 0,
    }
    
    return JsonResponse(stats)
