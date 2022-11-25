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
        sta_if.connect('VIVOFIBRA-1340', '3FA2466B77')
        while not sta_if.isconnected():
            pass # wait till connection
    print('network config:', sta_if.ifconfig())
    
connect_scfu()

HOST = "1.europe.pool.ntp.org"

def synchronize_ntp(callback_id, current_time, callback_memory):
    ntptime.host = HOST
    print('tempo sincronizado')
    ntptime.settime()
    
synchronize_ntp()

# mqtt client setup
CLIENT_NAME = 'pi-iv-a'
BROKER_ADDR = 'broker.hivemq.com'
mqttc = MQTTClient(CLIENT_NAME, BROKER_ADDR, keepalive=60)

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
        print(temp,"C de Temperatura")
        Umid = sensor.humidity()
        print(Umid,"% de Umidade")
        
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
  
    
    dict = {}                                                                                                                                                                                                   
    dict["Valor"] = temp
    dict["DataHora"] = datahora
    dict["Descricao"] = "Temperatura"
    dict["Origem"] = "Graciela"
    print(dict)
    
    publicacao_temp = ujson.dumps(dict)
    print(publicacao_temp)

    dict = {}                                                                                                                                                                                                   
    dict["Valor"] = Umid
    dict["DataHora"] = datahora
    dict["Descricao"] = "Umidade"
    dict["Origem"] = "Graciela"
    print(dict)
    
    publicacao_umid = ujson.dumps(dict)
    print(publicacao_umid)

    tentativas=0
    while(tentativas <= 10):
      try:
         mqttc.connect()
         mqttc.publish(BTN_TOPIC, publicacao_temp.encode())
         mqttc.publish(BTN_TOPIC, publicacao_umid.encode())
      except:
         time.sleep(5)
         tentativas=tentativas+1
     
    mqttc.disconnect()

mcron.init_timer()
#mcron.insert(mcron.PERIOD_MINUTE, 5), 'minute_5s', counter)
mcron.insert(mcron.PERIOD_HOUR, range(0, mcron.PERIOD_HOUR, mcron.PERIOD_HOUR // 6), 'day_x4', publica)
mcron.insert(mcron.PERIOD_DAY, range(0, mcron.PERIOD_DAY, mcron.PERIOD_DAY // 2), 'day_x2', synchronize_ntp)
