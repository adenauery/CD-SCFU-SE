import mysql.connector

minha_conexao_bd = mysql.connector.connect(host="scfu.exehda.org", user="scfur", passwd="XXXXXXXXXX", database="sensoriamento")
meu_cursor = minha_conexao_bd.cursor()

#    A password é a mesma utiliza no acesso abaixo:
#    http://scfu.exehda.org/phpmyadmin/
#    Utilizador: scfu
#    Palavra-passe: XXXXXXXXXXXX
#    Banco de Dados: sensoriamento


sql = ("SELECT * FROM publicacoes WHERE origem='Profa Fernanda' ORDER BY publicacoes.datahora DESC LIMIT 10")
meu_cursor.execute(sql)

minha_consulta = meu_cursor.fetchall()

print("\n|Ultimas 10 Temperaturas     |")
print("|Profa Fernanda              |")
for linha in minha_consulta:
  valor, datahora, descricao, origem, datahorautc = linha
  print("|", valor, "|", datahora,"|")

print("\n")
minha_conexao_bd.close()
