from machine import Pin
import dht
import ujson as json
from utils.mqtt import create_mqtt_client, create_topic
from utils.new_date import NewDate
from utils.measure_dht11 import measure_dht11

with open('config.json') as f:
    config = json.load(f)

MQTTC = create_mqtt_client(config['client_name'], config['broker_addr'])
BTN_TOPIC = create_topic(config['client_name'])

TEMPERATURE = "Temperatura"
HUMIDITY = "Umidade"
ORIGIN = "Wellington"


def get_payload(value, data, description):
    payload = {}

    payload["Valor"] = value
    payload["DataHora"] = data
    payload["Descricao"] = description
    payload["Origem"] = ORIGIN
    return json.dumps(payload)

def publish_dht11(callback_id, current_time, callback_memory):
    temperature, humidity = measure_dht11(23)
    date = NewDate()
  
    publish_temperature = get_payload(temperature, date.get_date, TEMPERATURE)
    publish_humidity = get_payload(humidity, date.get_date, HUMIDITY)
    
    MQTTC.connect()
    MQTTC.publish(BTN_TOPIC, publish_temperature.encode())
    MQTTC.publish(BTN_TOPIC, publish_humidity.encode())
    MQTTC.disconnect()