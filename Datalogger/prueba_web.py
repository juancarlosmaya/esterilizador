from envio_web  import Client
import json
import math
import time 

client = Client(server="http://esterilizacionremota.pythonanywhere.com/APIusuario/2/")
#client.EnviarDato(90)

# Get data from database
payload = client.GET()
print(payload)
if payload is not None:
    doc = json.loads(payload)
    print(doc['nombre'])

senal_antes = doc['presion']['senal']
print(senal_antes)
senal = senal_antes

x=0
while(1):
    for i in range(511):
        senal[i] = senal_antes[i + 1]
    x=x+1
    presion = 2*math.sin(x*2*math.pi/360)
    senal[511]=presion
    senal[511] = 0
    for j in range(511):
        doc["presion"]["senal"][j] = int(senal[j])
        doc["presion"]["senal"][j] = 100
        doc["pletismografia"]["senal"][j] = int(senal[j+1])
        doc["pletismografia"]["senal"][j] = 15
    payload = client.PUT(doc)
    senal_antes = senal
    time.sleep(0.7)
    

    #print(payload)
