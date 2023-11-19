import serial
import time

# Open the serial port
ser = serial.Serial('COM3', 9600)

# Create an empty dictionary to store the strings
data = {}

# Continuously read strings from the serial port and add them to the dictionary
while True:
    # Read a line of data from the serial port
    line = ser.readline().decode('utf-8').strip()

    # If the line is not empty, add it to the dictionary
    if line:
        # Get the current number of strings
        count = len(data)

        # Add the string to the dictionary with the count as the key
        data[count] = line

        # Print the current dictionary
        print(data)

        # Wait for a second before reading the next string
        time.sleep(1)
