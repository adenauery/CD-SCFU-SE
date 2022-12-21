from machine import Pin
import dht

TEMPERATURE = "Temperatura"
HUMIDITY = "Umidade"
ORIGIN = "Wellington"

def measure_dht11(pin):
    """
    Exemplo:
        measure_dht11(23)    

    :param pin: pino conectado a esp32.
    :type  value: int
    :return: 
        os valores medidos pelo DHT11.
    """
    sensor = dht.DHT11(Pin(pin))
    try:
        sensor.measure()
        temperature = sensor.temperature()
        humidity = sensor.humidity()
 
        return temperature, humidity

    except OSError as err:
        print("Falha na leitura dos dados")

  

