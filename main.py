from utils import project
import time
import paho.mqtt.client as mqtt
import json

clientId = "Contenedor 1"
port = 1883
host = "localhost"

client = mqtt.Client(clientId)
client.connect(host)


main = project()

# Diccionario Python
cliente = {
    "N_hielera": 1
}

# Obtener una cadena de caracteres JSON



while True:
    main.led_on('verde')
    humidity, temperature = main.read()
    # dic = {"Humedad" : humidity,"Temperatura" : temperature}
    # dic = json.loads(str(dic))
    # humidity, temperature = main.control_temp(2,8)
    main.lcd_write(f"Temp : {temperature} C  \nHumedad : {humidity} %")
    # client.publish("temperatura", f"Temp : {temperature} C  \nHumedad : {humidity} %")
    # client.publish("temperatura", f'{humidity},{temperature}')

    # client.publish("temperatura", temperature)
    # client.publish("humedad", humidity)

    cliente["Temperatura"] = temperature
    cliente["Humedad"] = humidity
    
    cliente_JSON = json.dumps(cliente)
    client.publish("pruebas", cliente_JSON)

    # main.lcd_write(f"T : {temperature} C  \n H : {humidity} %")
    time.sleep(1)