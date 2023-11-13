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

client = Client(server="http://lerdbiomedica.pythonanywhere.com/APIusuario/1/")

# Get data from database
payload = client.GET()
#print(payload)
if payload is not None:
    doc = json.loads(payload)
    print(doc['nombre'])

senal_antes = doc['pletismografia']['senal']
senal = senal_antes

x=0
while(1):
    for i in range(256):
        senal[i] = senal_antes[i + 1]
    x=x+1
    temperatura = 20*math.sin(x*2*math.pi/360)
    senal[256]=temperatura
    for j in range(256):
        doc["pletismografia"]["senal"][j] = int(senal[j])

    payload = client.PUT(doc)
    time.sleep(0.5)
    #print(payload)
