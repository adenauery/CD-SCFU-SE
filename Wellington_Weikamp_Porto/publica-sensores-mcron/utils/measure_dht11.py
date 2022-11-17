from machine import Pin
import dht

def measure_dht11(pin):
    sensor = dht.DHT11(Pin(pin))
    try:
        sensor.measure()
        temperature = sensor.temperature()
        humidity = sensor.humidity()
 
        return temperature, humidity

    except OSError as err:
        print("Falha na leitura dos dados")

  

