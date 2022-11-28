import mysql.connector

minha_conexao_bd = mysql.connector.connect(host="scfu.exehda.org", user="scfur", passwd="ucpelpelotas", database="sensoriamento")
meu_cursor = minha_conexao_bd.cursor()

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
