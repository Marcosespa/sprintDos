from ..models import Cronograma

def get_cronogramas():
    queryset = Cronograma.objects.all()
    return (queryset)

# def create_variable(form):
#     measurement = form.save()
#     measurement.save()
#     return ()