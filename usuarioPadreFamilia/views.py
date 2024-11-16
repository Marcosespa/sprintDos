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
    if role == "Gerente" or role=="Padre de Familia":
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
        if not role:  # Si no se puede obtener el rol
            messages.error(request, 'No se pudo verificar el rol del usuario.')
            return JsonResponse({'message': 'Error de autenticación'}, status=401)
        
        if role not in ["Padre de Familia", "Gerente"]:
            messages.error(request, 'No tiene permisos para acceder a esta página.')
            return JsonResponse({'message': 'Unauthorized User'}, status=403)
        
        try:
            usuario_padre = request.user
            pagos = Pago.objects.filter(usuario_padre=usuario_padre)
            
            # Calculate stats safely
            pagos_pendientes = pagos.filter(estado_pago='PENDIENTE').count()
            total_pagado = pagos.filter(estado_pago='PAGADO').aggregate(Sum('valor_pago'))['valor_pago__sum'] or 0
            
            context = {
                'pagos_pendientes_count': pagos_pendientes,
                'total_pagado': total_pagado,
                'role': role,  # Agregar el rol al contexto
            }
            return render(request, 'index_PadreFamilia.html', context)
            
        except Exception as e:
            messages.error(request, f'Error al obtener datos de pagos: {str(e)}')
            return JsonResponse({'message': 'Error al procesar la solicitud'}, status=500)
            
    except (IndexError, AttributeError) as e:
        messages.error(request, 'Error de autenticación')
        return JsonResponse({'message': 'Error de autenticación'}, status=401)

@login_required
def salir(request):
    logout(request)
    return redirect('https://dev-rgo1o3badtq3r0pa.us.auth0.com/v2/logout?returnTo=http%3A%2F%2F104.198.44.212:8080')

@login_required
def cronograma(request):
    return redirect('cronograma_index')

@login_required
def pago(request):
    return render(request, 'procesar_pago.html')
@login_required
def realizarpago(request):
    return render(request, 'realizar_pago.html')

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
