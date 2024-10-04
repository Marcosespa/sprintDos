from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.views.generic.edit import UpdateView
from usuarioPadreFamilia.models import UsuarioPadreFamilia


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