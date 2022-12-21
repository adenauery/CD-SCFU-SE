from umqtt.simple import MQTTClient

def create_mqtt_client(client_name, broker_addr):
    """
    Exemplo:
        create_mqtt_client(client_name, broker.hivemq.com)    

    :param client_name: nome do cliente MQTT.
    :type  value: string
    :param broker_addr: broker MQTT escolhido.
    :type  value: string
    :return: 
        a conexão MQTT.
    """
    return MQTTClient(client_name, broker_addr, keepalive=60)

def create_topic(client_name):
    """
    Exemplo:
        client_name(client_name)    

    :param client_name: nome do cliente MQTT.
    :type  value: string
    :return: 
        o Tópico criado.
    """
    return client_name.encode() + b'/dados'
