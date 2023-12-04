import serial
import time

import fpdf

# Create a new PDF document
pdf = fpdf.FPDF()
# Set the font
pdf.set_font('Arial', 'B', 10)
pdf.set_line_width(0.01)
# Add a page
pdf.add_page()



# Open the serial port
print("abriendo pueto")
try:
    ser = serial.Serial(port='COM7', bytesize=8, parity='E', baudrate = 19600, stopbits=1,timeout=0.5)
except:
    print("error")

print(ser)

# Create an empty dictionary to store the strings
data = {}
line2= ""

# Continuously read strings from the serial port and add them to the dictionary
for x in range(0,5):
    # Read a line of data from the serial port
    
    line = ser.read_until()                         # lectura de cadena recibida en binario                                
    line = line.decode('Latin-1').replace("\r", "\n") # conversion a cadena de texto, remplazando retorno de carro por nueva linea
    
    line2 = line2+line
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


    time.sleep(5)
    print("LA CANTIDAD DE BYTES ACUMULADOS SON: ")
    print(ser.in_waiting)
pdf.write(5,line2)
pdf.output('hello_world.pdf')

        