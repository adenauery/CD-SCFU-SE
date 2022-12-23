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
    sta_if = network.WLAN(network.STA_IF)  #conecta a um roteador
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect('VIVOFIBRA-1340', '?????????')
        while not sta_if.isconnected():
            pass # wait till connection
    print('network config:', sta_if.ifconfig())
    
connect_scfu()

def sincronizar_ntp (callbalck_id, current_time, callback_memory):
    ntptime.host = "1.europe.pool.ntp.org"  #pool.ntp.org é um grande cluster virtual.Fornece serviço NTP
    ntptime.settime()
    
ntptime.host = "1.europe.pool.ntp.org"
        
tentativas_ajuste_relogio=0
ajuste_relogio=0
while ajuste_relogio == 0 and tentativas_ajuste_relogio <= 20:
    try:
        ntptime.settime()  #ajusta o relogio. Precisa do servidor(rede)
        ajuste_relogio=1
        print("Relogio ajustado")
    except:
        time.sleep(5)
        tentativas_ajuste_relogio=tentativas_ajuste_relogio+1
        print("Tentativas ajuste relogio：%s" %str(tentativas_ajuste_relogio))
        ajuste_relogio=0

# Inicio da Configuracao do Cliente MQTT 

CLIENT_NAME = 'scfu'
BROKER_ADDR = 'broker.hivemq.com'
mqttc = MQTTClient(CLIENT_NAME, BROKER_ADDR, keepalive=60)

BTN_TOPIC = CLIENT_NAME.encode() + b'/dados'
print(BTN_TOPIC)

publicacao_temp=[]
publicacao_umid=[]

# Fim da Configuracao do Cliente MQTT 

indice_pub=0

def le_sensores (callback_id, current_time, callback_memory):
    global BTN_TOPIC
    global mqttc
    global CLIENT_NAME
    global BROKER_ADDR
    global indice_pub
    global publicacao_temp
    global publicacao_umid
    
    print(' ')
    print('Iniciou Le Sensores')
    
    sensor = dht.DHT22(Pin(23))
    try:
       sensor.measure()
       temp = sensor.temperature()
       #print(temp,"C de Temperatura")
       umid = sensor.humidity()
       #print(umid,"% de Umidade")
        
    except OSError as err:
       print("Falha na leitura dos dados")
  
    ano=time.localtime()[0]
    mes=time.localtime()[1]
    dia=time.localtime()[2]
    hora=time.localtime()[3]
    minuto=time.localtime()[4]
    segundo=time.localtime()[5]
    datahorautc=str(ano)+"-"+str(mes)+"-"+str(dia)+" "+str(hora)+ ":"+str(minuto)+ ":"+str(segundo)
    print(datahorautc)
  
    dict = {}                                                                                                                                                                                                   
    dict["Valor"] = temp
    dict["DataHora"] = datahorautc
    dict["Descricao"] = "Temperatura"
    dict["Origem"] = "Graciela"
    print(dict)
    
    pub_temp = ujson.dumps(dict)
    
    dict = {}                                                                                                                                                                                                   
    dict["Valor"] = umid
    dict["DataHora"] = datahorautc
    dict["Descricao"] = "Umidade"
    dict["Origem"] = "Graciela"
    print(dict)
    
    pub_umid = ujson.dumps(dict)
    
    try:
      mqttc.connect()
      mqttc.publish(BTN_TOPIC, pub_temp.encode())
      mqttc.disconnect()
     except:
      publicacao_temp.append(pub_temp)
   
    try:
      mqttc.connect()
      mqttc.publish(BTN_TOPIC, pub_umid.encode())
      mqttc.disconnect()
     except:
      publicacao_umid.append(pub_umid)
 
 
def publica_sensores (callback_id, current_time, callback_memory):
    global BTN_TOPIC
    global mqttc
    global CLIENT_NAME
    global BROKER_ADDR
    global publicacao_temp
    global publicacao_umid
    
    tentativas_publicacao_total=0
    print(' ')
    print('Iniciou Publica Sensores')
    
    while tentativas_publicacao_total <= 0 and ( len(publicacao_temp)  >  0 or   len(publicacao_umid)  >  0): 
        if len(publicacao_temp)  >  0:
            tentativas_publicacao=0
            publicacao=0
            while publicacao == 0 and tentativas_publicacao <= 0:
                try:
                    mqttc.connect()
                    mqttc.publish(BTN_TOPIC, publicacao_temp[0].encode())
                    mqttc.disconnect()
                    print(publicacao_temp[0])
                    publicacao_temp.pop(0)
                    publicacao=1   
                except:
                    time.sleep(5)
                    tentativas_publicacao=tentativas_publicacao+1
                    print("Tentativas publicacao temperatura：%s" %str(tentativas_publicacao))
                    publicacao=0
        if len(publicacao_umid)  >  0:
             tentativas_publicacao=0
             publicacao=0
             while publicacao == 0 and tentativas_publicacao <= 0:
                 try:
                     mqttc.connect()
                     mqttc.publish(BTN_TOPIC, publicacao_umid[0].encode())
                     mqttc.disconnect()
                     print(publicacao_umid[0])
                     publicacao_umid.pop(0)
                     publicacao=1   
                 except:
                     time.sleep(5)
                     tentativas_publicacao=tentativas_publicacao+1
                     print("Tentativas publicacao umidade：%s" %str(tentativas_publicacao))
                     publicacao=0
            
        tentativas_publicacao_total=tentativas_publicacao_total+1
        print("Tentativas publicacao total：%s" %str(tentativas_publicacao_total))
 
mcron.init_timer()
mcron.insert(mcron.PERIOD_HOUR, range(0, mcron.PERIOD_HOUR, mcron.PERIOD_HOUR // 6), 'day_x4', le_sensores)
mcron.insert(mcron.PERIOD_HOUR, range(0, mcron.PERIOD_HOUR, mcron.PERIOD_HOUR // 60), 'day_x6', publica_sensores)
mcron.insert(mcron.PERIOD_DAY, range(0, mcron.PERIOD_DAY, mcron.PERIOD_DAY // 2), 'day_x2', sincronizar_ntp)
