import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
import Adafruit_DHT
from gpiozero import LED

class project():
    def __init__(self, pin_DTH = 14, pin_led_rojo = 7, pin_led_amarillo = 1, pin_led_verde = 12):

        ## Configuración sensor de temperatura y humedad
        self.sensor_DTH11 = Adafruit_DHT.DHT11
        self.pin_DTH = pin_DTH

        ## Configuración LEDs
        self.leds = {
                            "rojo": LED(pin_led_rojo),
                            "amarillo": LED(pin_led_amarillo),
                            "verde": LED(pin_led_verde)
                        }

        ## Configuración de lcd

        # Tamaño de el LCD
        lcd_columns = 16
        lcd_rows = 2

        # Configuración de pines para LCD:
        lcd_rs = digitalio.DigitalInOut(board.D21)
        lcd_en = digitalio.DigitalInOut(board.D20)
        lcd_d4 = digitalio.DigitalInOut(board.D25)
        lcd_d5 = digitalio.DigitalInOut(board.D24)
        lcd_d6 = digitalio.DigitalInOut(board.D23)
        lcd_d7 = digitalio.DigitalInOut(board.D18)

        # Inicialización de clases LCD
        self.lcd = characterlcd.Character_LCD_Mono(
            lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows
        )

    def led_on(self, color):
        self.leds[color].on()
    def led_off(self,color):
        self.leds[color].off()

    def read(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor_DTH11, self.pin_DTH)
        return humidity, temperature
    
    def lcd_write(self, message):
        self.lcd.backlight
        self.lcd.message = message
    
    def control_temp(self, lim_down, lim_up):

        humidity, temperature = self.read()
        # print(humidity)
        # print(temperature)
        umbral = (lim_up - lim_down) / 3
        if (lim_down + umbral) <= temperature <= (lim_up - umbral):
            # print('verde')
            self.led_on('verde')
            self.led_off('amarillo')
            self.led_off('rojo')
        elif (lim_down) <= temperature < (lim_down + umbral) or (lim_up - umbral) < temperature <= (lim_up):
            # print('amarillo')
            self.led_on('amarillo')
            self.led_off('verde')
            self.led_off('rojo')
        else:
            # print('rojo')
            self.led_on('rojo')
            self.led_off('verde')
            self.led_off('amarillo')
        return humidity, temperature

class contenedor_virtual():
    def __init__(self,numero_hielera = 2,limite_temperatura = [27,0],limite_humedad = [30,80], muestras = 1000) -> None:
        self.limite_temperatura = limite_temperatura
        self.temp = list(np.linspace(limite_temperatura[0],limite_temperatura[1],int(muestras/2)))
        self.temp += list(reversed(self.temp))
        self.numero = numero_hielera

        self.hum = list(np.linspace(limite_humedad[0],limite_humedad[1],int(muestras/2)))
        self.hum += list(reversed(self.hum))

        self.contador = -1
        
    def lectura(self):
        self.contador += 1
        try:
            temperatura = int(self.temp[self.contador])
            humedad = int(self.hum[self.contador])
        except:
            self.contador = 0
            temperatura = int(self.temp[self.contador])
            humedad = int(self.hum[self.contador])

        cliente = {
            "N_hielera": self.numero,
            "vmin": 2,
            "vmax" : 8,
            "Temperatura" : temperatura,
            "Humedad" : humedad
        }
            
        return cliente