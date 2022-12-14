### Mestranda Graciela Barbosa Viana ###

Bem vindos ao meu diretório aonde serão registrados os códigos desenvolvidos para atendimento de demandas das disciplina de **Ciência de Dados na Internet das Coisas, Sistemas Embarcados e Sistemas Ciber Físicos e Ubíquos** do [MEEC](https://pos.ucpel.edu.br/ppgeec/) da UCPel.

Outras informações sobre a minha atuação como mestranda estão disponíveis na minha [short-bio](http://olaria.ucpel.edu.br/scfu/doku.php?id=graciela_barbosa_viana_short_bio)

#### Comentários Sobre os Softwares Desenvolvidos: ####


### Softwares Exemplo ###

  * **[ajusta-relogio.py](https://github.com/adenauery/micropython/blob/main/ajusta-relogio.py)**: ajusta o relógio da ESP32 utilizando o NTP (Network Time Protocol)
  * **[publica-sensores-sleep.py](https://github.com/adenauery/micropython/blob/main/publica-sensores-sleep.py)**: publica leituras feitas por sensores em JSON (DHT 22, no caso) utilizando o protocolo MQTT (biblioteca sem suporte a senha), com intervalo de publicação por sleep (sem agendamento). O programa tem impressões em vários pontos, as quais, quando em regime de produção, podem ser suprimidas.
  * **[instalar-mcron.py](https://github.com/adenauery/micropython/blob/main/instalar-mcron.py)**: instala a biblioteca mcron, utilizada para o agendamento de chamadas de procedimentos. Documentação disponível em: https://pypi.org/project/micropython-mcron/. No repositório da mcron, estão disponíveis diversas orientações adicionais: https://github.com/fizista/micropython-mcron/
  * **[le-imprime-bd-remoto.py ](https://github.com/adenauery/CD-SCFU-SE/blob/main/le-imprime-bd-remoto.py)**: lê um banco de dados remoto e imprime valores na tela
  
  
  Cliente Web para Protocolo MQTT
  * http://www.hivemq.com/demos/websocket-client/
  * Tópico em uso: scfu/dados
