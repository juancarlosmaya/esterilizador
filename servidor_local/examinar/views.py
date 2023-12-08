from django.shortcuts import render
from django.http import HttpResponse
import os
# Create your views here.
def listado_view(request):
    #DIRECTORIO= "/Users/JUAN CARLOS/Desktop/Esterilizador/Datalogger/REGISTROS"
    DIRECTORIO= "/Users/JUAN CARLOS/Desktop/Esterilizador/servidor_local/static/"
    registros=os.listdir(DIRECTORIO)
    print(registros)
    return render(request,"examinar/examinar.html",{'registros':registros})


    

def list_files(directory):
    files = os.listdir(directory)
    for file in files:
        print(file)