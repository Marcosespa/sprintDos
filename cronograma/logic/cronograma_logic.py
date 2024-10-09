from ..models import Cronograma

def get_cronogramas():
    queryset = Cronograma.objects.all()
    print(queryset)
    return (queryset)

# def create_variable(form):
#     measurement = form.save()
#     measurement.save()
#     return ()
#dedede