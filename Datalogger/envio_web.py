import json
import requests
import math
import time 


class Client:
    def __init__(self, server):
        self.server = server

    def GET(self):
        response = requests.get(self.server)
        if response.status_code > 0:
            return response.content
        return None

    def PUT(self, message):
        response = requests.put(self.server, data=json.dumps(message), headers={"Content-Type": "application/json"})
        if response.status_code > 0:
            return response.content
        return None
    
    def EnviarDato(self, temperatura, presion):
        payload = self.GET()
        if payload is not None:
            doc = json.loads(payload)
           
           # actualizar señal de temperatura
            senal_antes = doc['pletismografia']['senal']
            print(senal_antes)
            senal = senal_antes
            for i in range(255):
                senal[i] = senal_antes[i + 1]
            senal[255]=temperatura
            for j in range(255):
                doc["pletismografia"]["senal"][j] = int(senal[j])

            # actualizar señal de presion
            senal_antes = doc['presion']['senal']
            print(senal_antes)
            senal = senal_antes
            for i in range(255):
                senal[i] = senal_antes[i + 1]
            senal[255]=presion
            for j in range(255):
                doc["presion"]["senal"][j] = int(senal[j])

            # enviar señales de temperatura y presion
            payload = self.PUT(doc)
            time.sleep(0.5)
            return 
        return None


#client = Client(server="http://esterilizacionremota.pythonanywhere.com/APIusuario/2/")

# Get data from database
#payload = client.GET()
#print(payload)
#if payload is not None:
#    doc = json.loads(payload)
#    print(doc['nombre'])

#senal_antes = doc['pletismografia']['senal']
#print(senal_antes)
#senal = senal_antes

#x=0
#while(1):
#    for i in range(255):
#        senal[i] = senal_antes[i + 1]
#    x=x+1
#    temperatura = 20*math.sin(x*2*math.pi/360)
#    senal[255]=temperatura
#    for j in range(255):
#        doc["pletismografia"]["senal"][j] = int(senal[j])
#    payload = client.PUT(doc)
#    senal_antes = senal
#    time.sleep(0.5)
    

    #print(payload)
