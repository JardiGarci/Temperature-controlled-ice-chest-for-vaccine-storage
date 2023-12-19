# Importación de librerías
from utils import project
import time
import paho.mqtt.client as mqtt
import json

# Configuración de mqtt
clientId = "Contenedor 1"
port = 1883
host = "localhost"
client = mqtt.Client(clientId)
client.connect(host)

# Limites de temperatura y número de hielera
limite_inferior = 2
limite_superior = 8
numero_hielera = 1

# Importando sensores y actuadores del proyecto
main = project()

# Diccionario Python
cliente = {
    "N_hielera": numero_hielera,
    "vmin": limite_inferior,
    "vmax" : limite_superior
}

while True:

    # Lectura del sensor
    humidity, temperature = main.control_temp(2,8)

    # Escritura en la lcd
    main.lcd_write(f"Temp : {temperature} C  \nHumedad : {humidity} %")

    # Envío de información por mqtt
    cliente["Temperatura"] = temperature
    cliente["Humedad"] = humidity
    cliente_JSON = json.dumps(cliente)
    client.publish("TempHum", cliente_JSON)

    time.sleep(1)