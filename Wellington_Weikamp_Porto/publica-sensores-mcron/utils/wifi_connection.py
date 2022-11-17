import network
import ujson as json

with open('config.json') as f:
    config = json.load(f)

def connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect(config['ssid'], config['ssid_password'])
        while not sta_if.isconnected():
            pass # wait till connection
    print('network config:', sta_if.ifconfig())