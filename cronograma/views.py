from django.shortcuts import render
from .models import Cronograma
from django.shortcuts import render, get_object_or_404
from cronograma.models import Cronograma
from pago.models import Pago

def cronograma_index(request):
    cronogramas = Cronograma.objects.all() 
    return render(request, 'cronograma_index.html', {'cronograma_list': cronogramas})

def cronograma_list(request):
    cronogramas = [
        {'mes': 'Enero', 'valor_total': 150000, 'estado_pago': 'Pagado'},
        {'mes': 'Febrero', 'valor_total': 150000, 'estado_pago': 'Pendiente'}
    ]
    context = {
        'cronograma_list': cronogramas
    }
    return render(request, 'cronograma_index.html', context)


def pagos_filtrados(request):
    if request.method == "POST":
        # Obtener los datos del formulario
        mes = request.POST.get('mes')
        cronograma_id = request.POST.get('cronograma_id')

        # Obtener el cronograma específico
        cronograma = get_object_or_404(Cronograma, id=cronograma_id)

        # Filtrar los pagos por el mes y el cronograma
        pagos = Pago.objects.filter(fecha_pago__month=mes, cronograma=cronograma)

        # Renderizar la vista con los pagos filtrados
        return render(request, 'cronograma.html', {'cronograma': cronograma, 'pagos': pagos, 'mes': mes})

    # Si es un GET o algo inesperado, redirigir a la página de consulta
    return render(request, 'consulta_cronograma.html') 