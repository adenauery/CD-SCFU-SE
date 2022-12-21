import ntptime
from utils.ntp import HOST
import time

def synchronize_ntp(callback_id, current_time, callback_memory):
    """
    Função callback para sincronizar o tempo
    """
    ntptime.host = HOST
    while True:
        try:
            ntptime.settime()
            break
        except:
            time.sleep(5)