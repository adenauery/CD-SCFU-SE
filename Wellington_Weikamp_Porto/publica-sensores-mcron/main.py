from jobs.publish_dht11 import publish_dht11
from utils.ntp import synchronize_time
from utils.wifi_connection import connect
import mcron
import mcron.decorators


def main():
    connect()
    mcron.insert(mcron.PERIOD_DAY, range(0, mcron.PERIOD_DAY, mcron.PERIOD_DAY // 2), 'day_x2', synchronize_time)
    mcron.init_timer()
    mcron.insert(mcron.PERIOD_HOUR, range(0, mcron.PERIOD_HOUR, mcron.PERIOD_HOUR // 6), '10_min', publish_dht11)
    
  
if __name__ == '__main__':
    main()