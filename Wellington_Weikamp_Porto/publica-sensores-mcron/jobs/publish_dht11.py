import ujson as json
from jobs.led_warning import led_warning
from utils.mqtt import create_mqtt_client, create_topic
from utils.new_date import NewDate
from utils.measure_dht11 import measure_dht11, TEMPERATURE, HUMIDITY, ORIGIN

with open('config.json') as f:
    config = json.load(f)

MQTTC = create_mqtt_client(config['client_name'], config['broker_addr'])
BTN_TOPIC = create_topic(config['client_name'])

global publicacao_temp
global publicacao_umid

publish_temperature = []
publish_humidity = []

def get_payload(value, date, description):
    """
    Exemplo:
        get_payload(25, 2022-12-20 22:12:40, Temperatura)    

    :param value: valor da temperatura.
    :type  value: int
    :param date: data atual.
    :type  date: string
    :param description: descrição.
    :type  description: string
    :return: 
        o payload em JSON para publicação via MQTT.
    """
    payload = {}

    payload["Valor"] = value
    payload["DataHora"] = date
    payload["Descricao"] = description
    payload["Origem"] = ORIGIN
    return json.dumps(payload)

def publish_dht11(callback_id, current_time, callback_memory):
    """Função callback que publica os valores de temperatura e umidade."""
    temperature, humidity = measure_dht11(23)
    date = NewDate()
  
    publish_temperature.append(get_payload(temperature, date.get_date, TEMPERATURE))
    publish_humidity.append(get_payload(humidity, date.get_date, HUMIDITY))

    try:
        MQTTC.connect()
        for obj in publish_temperature:
            MQTTC.publish(BTN_TOPIC, obj.encode())
        for obj in publish_humidity:
            MQTTC.publish(BTN_TOPIC, obj.encode())
        MQTTC.disconnect()
        publish_temperature.clear()
        publish_humidity.clear()
        led_warning(5) 
    except:
        led_warning(2)
        with open('log.txt', 'a') as f:
            for obj in publish_temperature:
                f.write(f'{obj}\n')
            for obj in publish_humidity:
                f.write(f'{obj}\n')
            f.close()
    
    