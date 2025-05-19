#!/bin/bash
echo "hola servidor local"
source /home/juanc/esterilizador2/entorno_esterilizacion/Scripts/activate
cd /home/juanc/esterilizador2/servidor_local
python manage.py runserver 0.0.0.0:8000
read
