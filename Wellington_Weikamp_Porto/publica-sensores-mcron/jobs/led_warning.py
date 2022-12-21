from machine import Pin
from time import sleep


def led_warning(pin):
    """
    Exemplo:
        led_warning(22)    

    :param value: pino para conexão com o led.
    :type  value: int
    :return:
    """
    led = Pin(pin, Pin.OUT)
    led.value(1)
    sleep(2)
    led.value(0)
