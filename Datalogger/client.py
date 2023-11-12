import asyncio
#import serial
from pymodbus.client import AsyncModbusSerialClient
from pymodbus.framer.rtu_framer import ModbusRtuFramer

# Create a Modbus serial client
async def run():
    client = AsyncModbusSerialClient(port="COM1", framer = ModbusRtuFramer, baudrate=9600, bytesize = 8, parity= 'N', stopbits = 1)

    # Connect to the PLC
    await client.connect()

    # Read holding register 100 from slave address 1
    #result = client.read_holding_registers(88, 1, slave=1)

    #print(result)
    # Close the connection to the PLC
    client.close()

    # Check if the read operation was successful
    #if result.is_success():
        # Get the value of the holding register
    #    value = result.registers[0]

        # Print the value of the holding register to the console
    #    print(value)
    #else:
        # An error occurred while reading the holding register
    #    print(result.exception)

asyncio.run(run())