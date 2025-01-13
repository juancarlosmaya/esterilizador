from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import fitz  # PyMuPDF
import os
import datetime

# Create your views here.
def listado_view(request):
    #DIRECTORIO= "/Users/JUAN CARLOS/Desktop/Esterilizador/Datalogger/REGISTROS"
    DIRECTORIO= "/Esterilizador/servidor_local/static"
    registrosi=os.listdir(DIRECTORIO)
    print(registrosi)
    print("EL MEDIA ROOT ES:")
    print(str(settings.MEDIA_ROOT))

    registros = []
    fechas = []
    metadata_archivos = {} # Diccionario para almacenar metadatos
    for archivo in registrosi:
        if archivo.lower().endswith(".pdf"): # Verifica la extensión
            ruta_completa = os.path.join(DIRECTORIO, archivo)
            registros.append(archivo)
            try:
                doc = fitz.open(ruta_completa)
                metadata = doc.metadata
                metadata_archivos[archivo] = metadata # Guarda los metadatos
                print(f"Metadatos de {archivo}:")
                for clave, valor in metadata.items():
                    print(f"  {clave}: {valor}")
                fechas.append(datetime.datetime.strptime(metadata['creationDate'][2:-1], "%Y%m%d%H%M%S")) # Guarda la fecha de creación
                xmp_data = doc.xmp_metadata
                if xmp_data:
                    print("\nMetadatos XMP:")
                    print(xmp_data)
                doc.close() # Cierra el documento después de usarlo
            except fitz.fitz.FileDataError: #Manejo de error si el archivo no es un PDF válido
                print(f"Error: {archivo} no es un PDF valido o está corrupto")
            except Exception as e:
                print(f"Error al leer metadatos de {archivo}: {e}")
            registros_fechas = zip(registros, fechas)
    #return render(request,"examinar/examinar.html",{'registros':registrosi, 'fechas':fechas})
    return render(request,"examinar/examinar.html",{'registros_fechas':registros_fechas})


    

def list_files(directory):
    files = os.listdir(directory)
    for file in files:
        print(file)