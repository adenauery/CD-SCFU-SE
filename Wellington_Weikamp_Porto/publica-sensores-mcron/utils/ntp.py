import ntptime

HOST = "1.europe.pool.ntp.org"

def synchronize_time(callback_id, current_time, callback_memory):
    ntptime.host = HOST
    print('tempo sincronizado')
    ntptime.settime()