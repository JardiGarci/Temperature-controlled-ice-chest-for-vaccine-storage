import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
import Adafruit_DHT
from gpiozero import LED
# import time


class project():
    def __init__(self) -> None:

        ## Configuración sensor de temperatura y humedad
        self.sensor_DTH11 = Adafruit_DHT.DHT11
        self.pin_DTH = 14

        ## Configuración LEDs
        self.leds = {
                            "rojo": LED(7),
                            "amarillo": LED(1),
                            "verde": LED(12)
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

    def read(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor_DTH11, self.pin_DTH)
        return humidity, temperature
    
    def lcd_write(self, message):
        self.lcd.backlight
        self.lcd.message = message
    
    def control_temp(self, lim_down, lim_up):

        humidity, temperature = self.read()
        umbral = (lim_up - lim_down) / 3
        if (lim_down + umbral) <= temperature <= (lim_up - umbral):
            # print('verde')
            self.led_on('verde')
        elif (lim_down) <= temperature < (lim_down + umbral) or (lim_up - umbral) < temperature <= (lim_up):
            # print('amarillo')
            self.led_on('amarillo')
        else:
            # print('rojo')
            self.led_on('rojo')
        return humidity, temperature

# main = project()

# while True:
#     main.led_on('verde')
#     humidity, temperature = main.read()
#     main.lcd_write(f"Temp : {temperature} C  \nHumedad : {humidity} %")
#     time.sleep(1)