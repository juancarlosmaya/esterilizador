from envio_web import Client
client = Client(server="https://monitorizacionesterilizacion.pythonanywhere.com/APIesterilizador/1/")
client.EnviarDato(25, 100)
