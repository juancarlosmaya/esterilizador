#!/bin/bash
echo "hola Datalogger"
source /home/juanc/esterilizador2/entorno_esterilizacion/Scripts/activate
cd /home/juanc/esterilizador2/Datalogger
python lectura_plc.py
read