import serial
import time
import fpdf
import unicodedata
import fitz


PUERTO = 'COM7'             #WINDOWS
#PUERTO = '/dev/ttyUSB0'    #LINUX

DIRECTORIO= '..\servidor_local\static\ '    #WINDOWS
#DIRECTORIO= '../servidor_local/static'     #LINUX

NOMBRE_DE_ARCHCIVO="0"
# Open the serial port
print("abriendo pueto")
try:
    # ser = serial.Serial(port='COM7', bytesize=8, parity='E', baudrate = 19600, stopbits=1,timeout=0.5)
    ser = serial.Serial(port='COM28', bytesize=8, parity='E', baudrate = 115200, stopbits=1,timeout=0.5)
    ser_impresora = serial.Serial(port='COM7', bytesize=8, parity='N', baudrate = 115200, stopbits=1,timeout=0.5)

    while True:
        line2= ""
        line =""
        while not ("FECHA" in  line):
            print("...")
            line = ser.read_until()                             # lectura de cadena recibida en binario
            ser_impresora.write(line)                           # envio de informació leida del plc a impresora     
            line = line.decode('Latin-1').replace("\r", "\n")   # conversion a cadena de texto, remplazando retorno de carro por nueva linea
        
        print("TIENE LA PALABRA FECHA")
        NOMBRE_DE_ARCHCIVO = line.replace("\n", " ").replace(":", " ").replace("\n", " ").replace("/","-").split('<')[0]
        NOMBRE_DE_ARCHCIVO="".join(x for x in NOMBRE_DE_ARCHCIVO if x.isalnum())
        print(NOMBRE_DE_ARCHCIVO)
        
        # Metadatos del PDF a crear
        metadata = {
            'Title': NOMBRE_DE_ARCHCIVO,  # Usamos el nombre del archivo como título
            'Author': 'Nombre del Autor',  # Reemplaza con el autor real
            'Subject': 'Datos del Esterilizador',  # Reemplaza con el asunto real
            'Keywords': 'Tipo estrilizador, Marca, Modelo, serie',  # Reemplaza con palabras clave reales
            "Tipo de esterilizador": "Vapor", #opcional
            "Volumen": "150 L", #opcional
            "Marca": "MacroIngenio", #opcional
            "Modelo": "150P2",   # Reemplazar
            "Serie": "150P10FEB048RV",         # Reemplazar
            "Registro Sanitario": "2016DM-0815021", # Reemplazar
        }
        
        # Create a new PDF document
        pdf = fpdf.FPDF()
        # Set the font
        pdf.set_font('Arial', 'B', 10)
        pdf.set_line_width(0.01)
        # Add a page
        pdf.add_page()

        while not ("DESCARGA" in  line):
            print("LA CANTIDAD DE BYTES ACUMULADOS SON: ")
            print(ser.in_waiting)
            line2 = line2+line
            line = ser.read_until()                             # lectura de cadena recibida en binario 
            ser_impresora.write(line)                           # envio de informació leida del plc a impresora
            line = line.decode('Latin-1').replace("\r", "\n")   # conversion a cadena de texto, remplazando retorno de carro por nueva linea
            time.sleep(0.5)

        print("TIENE LA PALABRA DESCARGA")

        line2 = line2+line
        
        pdf.write(5,line2)

        pdf.output("..\servidor_local\static\ "+ NOMBRE_DE_ARCHCIVO +".pdf")
        
        # Añadir metadatos con PyMuPDF
        try:
            doc = fitz.open(ruta_completa)
            doc.set_metadata(metadata)
            doc.save(ruta_completa)
            doc.close()
            print(f"Metadatos añadidos a {NOMBRE_DE_ARCHCIVO}.pdf")
        except Exception as e:
             print(f"Error al agregar metadatos con pymupdf: {e}")
        
        time.sleep(0.5)
except:
    print("error")

print(ser)







# Create an empty dictionary to store the strings
#data = {}


# Continuously read strings from the serial port and add them to the dictionary
#for x in range(0,5):
    # Read a line of data from the serial port
    
    
    
    
    #pdf.multi_cell(0,10,line)
    #if line:
    #    pdf.write(10,line)
    #    pdf.output('hello_world.pdf')
#        pdf.write(10,line)

    #    pdf.multi_cell(0, 10, line, 0, 'L', False)
        # Retrieve the current cursor position after the first multi-cell
    #    x_pos = pdf.get_x()
    #    y_pos = pdf.get_y()
        #  Set the cursor position for the second multi-cell
    #    pdf.set_xy(x_pos, y_pos + 10)

    #    pdf.multi_cell(0, 10, line, 0, 'L', False)
        

    #lines = line.splitlines()                       # creaciión de diccionario
    #dictionary = dict(enumerate(lines))
    
    #data.update(dictionary)                         # actualizaciçón de diccionario
    #print(data)

    #for i in data:# Add text to the page
    #    pdf.cell(40, 10, data[i], 0, ln=1)
        # Output the PDF
    #    pdf.output('hello_world.pdf')


#    time.sleep(5)
    


        