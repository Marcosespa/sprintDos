from django.shortcuts import render
from .models import Cronograma

def cronograma_index(request):
    cronogramas = Cronograma.objects.all() 
    return render(request, 'cronograma_index.html', {'cronogramas': cronogramas})

def cronograma_list(request):
    cronogramas = [
        {'mes': 'Enero', 'valor_total': 150000, 'estado_pago': 'Pagado'},
        {'mes': 'Febrero', 'valor_total': 150000, 'estado_pago': 'Pendiente'}
    ]
    context = {
        'cronograma_list': cronogramas
    }
    return render(request, 'cronograma_index.html', context)