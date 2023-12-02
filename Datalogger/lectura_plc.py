import serial
import time

# Open the serial port
print("abriendo pueto")
try:
    ser = serial.Serial(port='COM7', bytesize=8, parity='E', baudrate = 19600, stopbits=1,timeout=0.5)
except:
    print("error")

print(ser)

# Create an empty dictionary to store the strings
data = {}

# Continuously read strings from the serial port and add them to the dictionary
while True:
    # Read a line of data from the serial port
    
    line = ser.readline()
    print(line)
    line = line.decode('utf-8')
    print(line)
    line = line.strip()
    print(line)
    # If the line is not empty, add it to the dictionary
    if line:
        # Get the current number of strings
        count = len(data)

        # Add the string to the dictionary with the count as the key
        data[count] = line

        # Print the current dictionary
        print(data)

        # Wait for a second before reading the next string
        time.sleep(0.5)
