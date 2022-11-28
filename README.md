## Ciência de Dados na IoT, Sistemas Embarcados e Sistemas Ciber Físicos e Ubíquos ##

Este repositório registra os códigos desenvolvidos pela turma de mestrandos que está cursando as disciplinas de **Ciência de Dados na Internet das Coisas, Sistemas Embarcados e Sistemas Ciber Físicos e Ubíquos** do [MEEC](https://pos.ucpel.edu.br/ppgeec/) da UCPel.

As soluções são desenvolvidas em **Micropython** sobre a plataforma de hardware **ESP332**

### Softwares Desenvolvidos Pela Turma: ###

* [Gilson Viana Corrêa](https://github.com/adenauery/CD-SCFU-SE/tree/main/Gilson_Viana_Correa)
* [Graciela Barbosa Viana](https://github.com/adenauery/CD-SCFU-SE/tree/main/Graciela_Barbosa_Viana)
* [Karen Rediess Müller Sória](https://github.com/adenauery/CD-SCFU-SE/tree/main/Karen_Rediess_Muller_Soria)
* [Tiago Azevedo Appolinario da Silva](https://github.com/adenauery/CD-SCFU-SE/tree/main/Tiago_Azevedo_Appolinario_da_Silva)
* [Wellington Weikamp Porto](https://github.com/adenauery/Micropython/tree/main/Wellington_Weicamp_Porto)


### Softwares Exemplo ###

  * **[ajusta-relogio.py](https://github.com/adenauery/micropython/blob/main/ajusta-relogio.py)**: ajusta o relógio da ESP32 utilizando o NTP (Network Time Protocol)
  * **[publica-sensores-sleep.py](https://github.com/adenauery/micropython/blob/main/publica-sensores-sleep.py)**: publica leituras feitas por sensores em JSON (DHT 22, no caso) utilizando o protocolo MQTT (biblioteca sem suporte a senha), com intervalo de publicação por sleep (sem agendamento). O programa tem impressões em vários pontos, as quais, quando em regime de produção, podem ser suprimidas.
  * **[instalar-mcron.py](https://github.com/adenauery/micropython/blob/main/instalar-mcron.py)**: instala a biblioteca mcron, utilizada para o agendamento de chamadas de procedimentos. Documentação disponível em: https://pypi.org/project/micropython-mcron/. No repositório da mcron, estão disponíveis diversas orientações adicionais: https://github.com/fizista/micropython-mcron/
  * **[le-imprime-bd-remoto.py ](https://github.com/adenauery/CD-SCFU-SE/blob/main/le-imprime-bd-remoto.py)**: le banco de dados remoto e imprime valores na tela

### Alguns dos Materiais Utilizados na Concepção dos Códigos: ###
  
  * [Sistema Embarcado com ESP32 e MicroPython - Prof. Marcos Carnevali](https://www.youtube.com/playlist?list=PLCcdteC1rwSFvJnUoe0DfORHv4p_1EFps)
  * [Secrets of MicroPython: MQTT on ESP32](https://bhave.sh/micropython-mqtt/)
  * [ESP32 MicroPython: Encoding JSON](https://techtutorialsx.com/2017/05/27/esp32-micropython-encoding-json/)
  * [Boot Scripts - boot.py e main.py](https://learn.adafruit.com/micropython-basics-load-files-and-run-code/boot-scripts)
  * [Quick reference for the ESP32 - Site Micropython](https://docs.micropython.org/en/latest/esp32/quickref.html)
  
  
Cliente Web para Protocolo MQTT
  * http://www.hivemq.com/demos/websocket-client/
  * Tópico em uso: scfu/dados
