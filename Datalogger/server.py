import asyncio
import serial
from pymodbus.server import StartAsyncSerialServer
from pymodbus.datastore import (
    ModbusSequentialDataBlock,
    ModbusServerContext, 
    ModbusSlaveContext)


datablock  = ModbusSequentialDataBlock.create()
context = ModbusSlaveContext(
                di=datablock, co=datablock, hr=datablock, ir=datablock
            )
contexto = ModbusServerContext(slaves=context, single=True)

async def run_async_server(contexto):
    
    # Create a Modbus serial server
    server = await StartAsyncSerialServer(
        context= contexto,  # Data storage
        # identity=args.identity,  # server identify
        # timeout=1,  # waiting time for request to complete
        port= "COM7",  # serial port
        bytesize = 8, 
        parity= 'N', 
        stopbits = 1,
        # custom_functions=[],  # allow custom handling
        framer= "rtu",  # The framer strategy to use
        # stopbits=1,  # The number of stop bits to use
        # bytesize=8,  # The bytesize of the serial messages
        # parity="N",  # Which kind of parity to use
        baudrate=9600,  # The baud rate to use for the serial device
        # handle_local_echo=False,  # Handle local echo of the USB-to-RS485 adaptor
        # ignore_missing_slaves=True,  # ignore request to a missing slave
        # broadcast_enable=False,  # treat slave_id 0 as broadcast address,
        # strict=True,  # use strict timing, t1.5 for Modbus RTU
    )
    # await StartAsyncSerialServer()

asyncio.run(run_async_server(contexto))


print("hola")