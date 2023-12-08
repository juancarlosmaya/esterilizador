import serial
import time
import fpdf
import unicodedata



NOMBRE_DE_ARCHCIVO="0"
# Open the serial port
print("abriendo pueto")
try:
    ser = serial.Serial(port='COM7', bytesize=8, parity='E', baudrate = 19600, stopbits=1,timeout=0.5)
    
    while True:
        line2= ""
        line =""
        while not ("FECHA" in  line):
            print("...")
            line = ser.read_until()                             # lectura de cadena recibida en binario                                
            line = line.decode('Latin-1').replace("\r", "\n")   # conversion a cadena de texto, remplazando retorno de carro por nueva linea
        
        print("TIENE LA PALABRA FECHA")
        NOMBRE_DE_ARCHCIVO = line.replace("\n", " ").replace(":", " ").replace("\n", " ").replace("/","-").split('<')[0]
        NOMBRE_DE_ARCHCIVO="".join(x for x in NOMBRE_DE_ARCHCIVO if x.isalnum())
        print(NOMBRE_DE_ARCHCIVO)
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
            line = line.decode('Latin-1').replace("\r", "\n")   # conversion a cadena de texto, remplazando retorno de carro por nueva linea
            time.sleep(0.5)

        print("TIENE LA PALABRA DESCARGA")

        line2 = line2+line
        
        pdf.write(5,line2)

        pdf.output("..\servidor_local\static\ "+ NOMBRE_DE_ARCHCIVO +".pdf")
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
    


        