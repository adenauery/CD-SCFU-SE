from machine import Pin
from time import sleep
import ujson
import time
import ntptime
import dht
import utime
import mcron
import mcron.decorators
from umqtt.simple import MQTTClient

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


def sincronizar_ntp (callbalck_id, current_time, callback_memory):
    ntptime.host = "1.europe.pool.ntp.org"
    ntptime.settime()
    
ntptime.host = "1.europe.pool.ntp.org"
        
tentativas_ajuste_relogio=0
ajuste_relogio=0
while ajuste_relogio == 0 and tentativas_ajuste_relogio <= 20:
    try:
        ntptime.settime()
        ajuste_relogio=1
        print("Relogio ajustado")
    except:
        time.sleep(5)
        tentativas_ajuste_relogio=tentativas_ajuste_relogio+1
        print("Tentativas ajuste relogio：%s" %str(tentativas_ajuste_relogio))
        ajuste_relogio=0

# mqtt client setup
CLIENT_NAME = 'scfu'
BROKER_ADDR = 'broker.hivemq.com'
mqttc = MQTTClient(CLIENT_NAME, BROKER_ADDR, keepalive=60)

BTN_TOPIC = CLIENT_NAME.encode() + b'/dados'
print(BTN_TOPIC)
### -----------------------

indice_pub=0

def le_sensores (callback_id, current_time, callback_memory):
    global BTN_TOPIC
    global mqttc
    global CLIENT_NAME
    global BROKER_ADDR
    global indice_pub
    global publicacao_temp
    global publicacao_umid
    
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
    minuto=time.localtime()[4]
    segundo=time.localtime()[5]
    datahora=str(ano)+"-"+str(mes)+"-"+str(dia)+" "+str(hora)+ ":"+str(minuto)+ ":"+str(segundo)
    print(datahora)
    datahorautc = time.localtime()
    print(datahorautc)
   
    dict = {}                                                                                                                                                                                                   
    dict["Valor"] = temp
    dict["DataHora"] = datahora
    dict["Descricao"] = "Temperatura"
    dict["Origem"] = "Graciela"
    print(dict)
    
    indice_pub=indice_pub+1
    print("indice_pub leitura：%s" %str(indice_pub))
    
    publicacao_temp[indice_pub] = ujson.dumps(dict)
    print(publicacao_temp[indice_pub])

    dict = {}                                                                                                                                                                                                   
    dict["Valor"] = Umid
    dict["DataHora"] = datahora
    dict["Descricao"] = "Umidade"
    dict["Origem"] = "Graciela"
    print(dict)
    
    publicacao_umid[indice_pub] = ujson.dumps(dict)
    print(publicacao_umid[indice_pub])

    
def publica_sensores (callback_id, current_time, callback_memory):
    global BTN_TOPIC
    global mqttc
    global CLIENT_NAME
    global BROKER_ADDR
    global indice_pub
    global publicacao_temp
    global publicacao_umid

    time.sleep(5)
    tentativas_publicacao=0
    publicacao=0
    while indice_pub > 0:
      while publicacao == 0 and tentativas_publicacao <= 20:
          try:
            mqttc.connect()
            publicacao=1   
          except:
            time.sleep(5)
            tentativas_publicacao=tentativas_publicacao+1
            print("Tentativas：%s" %str(tentativas_publicacao))
            publicacao=0
      mqttc.publish(BTN_TOPIC, publicacao_temp[indice_pub].encode())
      mqttc.publish(BTN_TOPIC, publicacao_umid[indice_pub].encode())
      mqttc.disconnect()
      indice_pub=indice_pub-1
      print("indice_pub publicacao：%s" %str(indice_pub))
mcron.init_timer()
mcron.insert(mcron.PERIOD_HOUR, range(0, mcron.PERIOD_HOUR, mcron.PERIOD_HOUR // 60), 'day_x4', le_sensores)
mcron.insert(mcron.PERIOD_HOUR, range(0, mcron.PERIOD_HOUR, mcron.PERIOD_HOUR // 60), 'day_x5', publica_sensores)
mcron.insert(mcron.PERIOD_DAY, range(0, mcron.PERIOD_DAY, mcron.PERIOD_DAY // 2), 'day_x2', sincronizar_ntp)
