import datetime
import fitz
import time

NOMBRE_DE_ARCHCIVO = "0"  # El archivo se llamará 0.pdf

# Metadatos del archivo a crear
metadata = {
    'author' : 'Esterilizador a vapor, Modelo: 150P2, Serie: 150P10FEB048RV',
    'title' : 'Trazabilidad esterilización',
    'subject': 'Ciclo de esterilización 1',  
    'creator' : 'MacroIngenio',
    'keywords' : 'tipo:vapor,Modelo:150P2,Serie:150P10FEB048RV',
    'creationDate' : '' ## se asigna más abajo
}

# Ciclo que escribe una linea Hola mundo cada segundo en el archivo 0.pdf
line = ""
while True:
    line = line + "Hola mundo \n"
   
    doc = fitz.open()
    page = doc.new_page()
    p = fitz.Point(50, 50)  # start point of 1st line

    rc = page.insert_text(p,  # bottom-left of 1st char
                     line,  # the text (Holam mundo '\n')
                     fontname = "helv",  # the default font
                     fontsize = 8,  # the default font size
                     rotate = 0,  # also available: 90, 180, 270
                     )

    today = datetime.datetime.now(datetime.timezone.utc)
    
    metadata["creationDate"] = today.strftime("D:%Y%m%d%H%M%S")

    print(metadata)
    doc.set_metadata(metadata)
    doc.save("..\\servidor_local\\static\\" + NOMBRE_DE_ARCHCIVO + ".pdf")
    doc.close()

    time.sleep(1)