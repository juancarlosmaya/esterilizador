echo "hola"
source esterilizador2/entorno_esterilizacion/Scripts/activate 
cd esterilizador2/Datalogger/
python lectura_plc.py &
cd ..
cd servidor_local
python manage.py runserver 0.0.0.0:8000 

