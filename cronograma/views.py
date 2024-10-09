from django.shortcuts import render
from .models import Cronograma

def cronograma_index(request):
    cronogramas = Cronograma.objects.all() 
    return render(request, 'cronograma_index.html', {'cronogramas': cronogramas})

def cronograma_list(request):
    Cronogramas = get_cronogramas()
    context = {
        'cronograma_list': Cronogramas
    }
    return render(request, 'cronograma_index.html', context)