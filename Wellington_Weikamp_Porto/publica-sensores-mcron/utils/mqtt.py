from umqtt.simple import MQTTClient

def create_mqtt_client(client_name, broker_addr):
    return MQTTClient(client_name, broker_addr, keepalive=60)

def create_topic(client_name):
    return client_name.encode() + b'/dados'
