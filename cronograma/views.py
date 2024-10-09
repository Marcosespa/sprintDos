from django.shortcuts import render
from .models import Cronograma

def cronograma_index(request):
    cronogramas = Cronograma.objects.all() 
    return render(request, 'cronograma_index.html', {'cronogramas': cronogramas})

def cronograma_list(request):
    cronogramas = get_cronogramas()
    context = {
        'cronograma_list': cronogramas
    }
    return render(request, 'cronograma_index.html', context)