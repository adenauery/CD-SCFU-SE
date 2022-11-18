from umqtt.simple import MQTTClient
from machine import Pin
from time import sleep
import ujson
import time
import ntptime
import dht
import utime
import mcron
import mcron.decorators

def connect_scfu():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect('APT_301_2G', 'a1b1c1a2')
        while not sta_if.isconnected():
            pass # wait till connection
    print('network config:', sta_if.ifconfig())

connect_scfu()

ntptime.host = "1.europe.pool.ntp.org"
ntptime.settime()

# mqtt client setup
CLIENT_NAME = 'pi-iv-a'
BROKER_ADDR = 'broker.hivemq.com'
mqttc = MQTTClient(CLIENT_NAME, BROKER_ADDR, keepalive=60)
#mqttc.connect()

BTN_TOPIC = CLIENT_NAME.encode() + b'/dados'
print(BTN_TOPIC)
### -----------------------

def publica(callback_id, current_time, callback_memory):
    global BTN_TOPIC
    global mqttc
    global CLIENT_NAME
    global BROKER_ADDR

    sensor = dht.DHT22(Pin(23))
    try:
        sensor.measure()
        temp = sensor.temperature()
        print(temp)
        Umid = sensor.humidity()
        print(Umid)

    except OSError as err:
        print("Falha na leitura dos dados")

    ano=time.localtime()[0]
    mes=time.localtime()[1]
    dia=time.localtime()[2]
    hora=time.localtime()[3]
    hfl=[21,22,23,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    horalocal=hfl[hora]
    minuto=time.localtime()[4]
    segundo=time.localtime()[5]
    datahora=str(ano)+"-"+str(mes)+"-"+str(dia)+" "+str(horalocal)+ ":"+str(minuto)+ ":"+str(segundo)
    print(datahora)

    temperatura_dict = {}
    umidade_dict = {}
    temperatura_dict ["Valor"] = temp
    temperatura_dict ["DataHora"] = datahora
    temperatura_dict ["Descricao"] = "Temperatura"
    temperatura_dict ["Origem"] = "Tiago"

    umidade_dict ["Valor"] = Umid
    umidade_dict ["DataHora"] = datahora
    umidade_dict ["Descricao"] = "Umidade"
    umidade_dict ["Origem"] = "Tiago"

    publicacao_temperatura = ujson.dumps(temperatura_dict)
    publicacao_umidade = ujson.dumps(umidade_dict)

    mqttc.connect()
    mqttc.publish( BTN_TOPIC, publicacao_temperatura.encode() )
    mqttc.publish( BTN_TOPIC, publicacao_umidade.encode() )
    mqttc.disconnect()


    #sleep(600)
mcron.init_timer()
#mcron.insert(mcron.PERIOD_MINUTE, range(0, mcron.PERIOD_MINUTE, 180), 'minute_5s', counter)
mcron.insert(mcron.PERIOD_HOUR, range(0, mcron.PERIOD_HOUR, mcron.PERIOD_HOUR // 6), 'day_x4', publica)
