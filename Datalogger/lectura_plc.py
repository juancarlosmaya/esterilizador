import serial
import time
import datetime
import fitz
import pytz
import re
from envio_web import Client

client = Client(server="http://esterilizacionremota.pythonanywhere.com/APIusuario/2/")

# Nombre del PDF a crear
NOMBRE_DE_ARCHIVO = "0"

# Metadatos del PDF a crear
metadata = {
    'author' : 'Esterilizador a vapor, Modelo: 150P2, Serie: 150P10FEB048RV',
    'title' : 'Trazabilidad esterilización',
    'subject': 'Ciclo de esterilización',  
    'creator' : 'MacroIngenio',
    'keywords' : 'tipo:vapor,Modelo:150P2,Serie:150P10FEB048RV,Volumen:150 L,Registro_Sanitario:INVIMA 2017DM-0016011',
    'creationDate' : '' ## se asigna más abajo
}

# Ubicación del PDF a crear
DIRECTORIO= '..\servidor_local\static\ '    #WINDOWS
#DIRECTORIO= '..//servidor_local//static//'     #LINUX

## puerto de comunicacion con PLC
PUERTO_PLC = 'COM28'             #WINDOWS
#PUERTO_PLC = '/dev/ttyUSB0'    #LINUX

## puerto de comunicacion con impresora, quitar comentarios más abajo
#PUERTO_IMPRESORA = '/dev/ttyUSB1'    #LINUX

def guardar_pdf(texto):
    doc = fitz.open()
    page = doc.new_page()
    
    p = fitz.Point(50, 50)  # start point of 1st line
    rc = page.insert_text(p,  # bottom-left of 1st char
                texto,  # the text (Holam mundo '\n')
                fontname = "helv",  # the default font
                fontsize = 8,  # the default font size
                rotate = 0,  # also available: 90, 180, 270
            )
    print(texto)
    try:
        # Definir la zona horaria de Colombia
        colombia_timezone = pytz.timezone('America/Bogota')

        # Obtener la hora actual en Colombia
        today = datetime.datetime.now(colombia_timezone)

        #today = datetime.datetime.now(datetime.timezone.utc)
        metadata["creationDate"] = today.strftime("D:%Y%m%d%H%M%S")
        print(metadata)
        doc.set_metadata(metadata)
        doc.save("..\\servidor_local\\static\\" + NOMBRE_DE_ARCHIVO + ".pdf")
        doc.close()
    except Exception as e:
        print(f"Error al agregar metadatos con pymupdf: {e}")

    return


print("abriendo pueto")
try:
    #ser = serial.Serial(port='COM7', bytesize=8, parity='E', baudrate = 19600, stopbits=1,timeout=0.5)
    ser = serial.Serial(port=PUERTO_PLC, bytesize=8, parity='E', baudrate = 115200, stopbits=1,timeout=0.5)
    #ser_impresora = serial.Serial(port=PUERTO_IMPRESORA, bytesize=8, parity='N', baudrate = 115200, stopbits=1,timeout=0.5)

    while True:
        line2= ""
        line =""

        while not ("FECHA" in  line):
            print("...")
            line = ser.read_until()                             # lectura de cadena recibida en binario
            #ser_impresora.write(line)                           # envio de informació leida del plc a impresora     
            line = line.decode('Latin-1').replace("\r", "\n")   # conversion a cadena de texto, remplazando retorno de carro por nueva linea
        
        print("TIENE LA PALABRA FECHA")

        NOMBRE_DE_ARCHIVO = line.replace("\n", " ").replace(":", " ").replace("\n", " ").replace("/","-").split('<')[0]
        NOMBRE_DE_ARCHIVO = "".join(x for x in NOMBRE_DE_ARCHIVO if x.isalnum())
        print(NOMBRE_DE_ARCHIVO)
        match = re.search(r'CICLON(\d+)', NOMBRE_DE_ARCHIVO)
        if match:
            numero_ciclo = match.group(1)
        else:
            numero_ciclo =  " sin numero de ciclo"

        NOMBRE_DE_ARCHIVO = "Ciclo No. " + numero_ciclo

        while not ("DESCARGA" in  line):
            print("LA CANTIDAD DE BYTES ACUMULADOS SON: ")
            print(ser.in_waiting)
            line2 = line2 +line
            guardar_pdf(line2)
            time.sleep(0.5)
            line = ser.read_until() 
            match = re.search(r'TEMP:\s*(\d+)\s*øC\s*P:\s*(\d+)\s*kpa', line.decode('Latin-1'))
            if match:
                temperatura = int(match.group(1))  # Extraer temperatura como entero
                presion = int(match.group(2))  # Extraer presión como entero
                print(f"Temperatura: {temperatura}°C, Presión: {presion} kPa")
                client.EnviarDato(temperatura,presion)                           
            #ser_impresora.write(line)                           # envio de informació leida del plc a impresora
            line = line.decode('Latin-1').replace("\r", "\n")   # conversion a cadena de texto, remplazando retorno de carro por nueva linea
            print(line)

            

        print("TIENE LA PALABRA DESCARGA")
        line2 = line2 +line
        guardar_pdf(line2)
        
        
        time.sleep(0.5)
except Exception as e:
    print(f"Error: {e}")
    



