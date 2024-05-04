from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import os
# Create your views here.
def listado_view(request):
    #DIRECTORIO= "/Users/JUAN CARLOS/Desktop/Esterilizador/Datalogger/REGISTROS"
    DIRECTORIO= "/Esterilizador/servidor_local/static"
    registros=os.listdir(DIRECTORIO)
    print(registros)
    print("EL MEDIA ROOT ES:")
    print(str(settings.MEDIA_ROOT))
    return render(request,"examinar/examinar.html",{'registros':registros})


    

def list_files(directory):
    files = os.listdir(directory)
    for file in files:
        print(file)