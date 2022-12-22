from jobs.publish_dht11 import publish_dht11
from jobs.synchronize_ntp import synchronize_ntp
from jobs.remove_log import remove_log
from utils.wifi_connection import connect
import mcron
import mcron.decorators

def main():
    connect()
    mcron.init_timer()
    mcron.insert(mcron.PERIOD_HOUR, range(0, mcron.PERIOD_HOUR, mcron.PERIOD_HOUR // 6), 'day_x6', publish_dht11)
    mcron.insert(mcron.PERIOD_DAY, range(0, mcron.PERIOD_DAY, mcron.PERIOD_DAY), 'day_x1', remove_log)

if __name__ == '__main__':
    main()