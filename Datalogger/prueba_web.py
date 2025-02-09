from web  import Client

client = Client(server="http://esterilizacionremota.pythonanywhere.com/APIusuario/2/")
client.EnviarDato(90)
