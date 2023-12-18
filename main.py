from utils import project
import time
import paho.mqtt.client as mqtt
import json

clientId = "Contenedor 1"
port = 1883
host = "localhost"

limite_inferior = 2
limite_superior = 8

client = mqtt.Client(clientId)
client.connect(host)


main = project()

# Diccionario Python
cliente = {
    "N_hielera": 1,
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