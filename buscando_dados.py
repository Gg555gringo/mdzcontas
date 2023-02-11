import psycopg2

import datetime

def day_atual():
  day_atual = datetime.datetime.now()
  return day_atual



url = "postgres://admin:RNAYSKemijEuLPJetaN1MFdrm0GDGL2h@w0cmaz.stackhero-network.com:5432/admin?sslmode=require"
conn = psycopg2.connect(url)
cursor = conn.cursor()

def gerar_email():
    ...
    

def update_valores(tipo, valor):
    cursor.execute(f"UPDATE valores SET valor = {valor} WHERE tipo = '{tipo}'")
    conn.commit()

def adicionar_conta(conta, email, senha, tela, pin):
  cursor.execute(f"INSERT INTO contas(id, email, senha, tipo, tela, pin) VALUES(DEFAULT, '{email}', '{senha}', '{conta}', '{tela}', {pin})")
  conn.commit()

def verificar_tipo(conta):
  try:
    cursor.execute(f"SELECT valor FROM valores WHERE tipo = '{conta}'")
    if cursor.fetchone() == None:
      return False
    else:
      return True
  except:
    cursor.execute("ROLLBACK")
    conn.commit()
def diminuir_saldo(chat_id, saldo):
  sql = f"UPDATE usuarios SET saldo = {saldo} WHERE chat_id = {chat_id}"
  cursor.execute(sql)
  conn.commit()

def deletar_admin(chat_id):
  sql = f"DELETE FROM admins WHERE chat_id = {chat_id}"
  cursor.execute(sql)
  conn.commit()
  
def adicionar_admin(chat_id):
  sql = f"INSERT INTO admins(id, chat_id) VALUES(DEFAULT, {chat_id})"
  cursor.execute(sql)
  conn.commit()

def verificar_call(id_clicado, id_usuario):
  if id_clicado == id_usuario:
    ...
  else:
    return False

def verificar_admin(chat_id):
  try:
    sql = f"SELECT id FROM admins WHERE chat_id = {chat_id}"
    cursor.execute(sql)
    if cursor.fetchone() == None:
      return False
    else: 
      return True
  except:
    cursor.execute("ROLLBACK")
    conn.commit()
def verificar_existe(chat_id):
    try:
      cursor.execute( f"SELECT saldo FROM usuarios WHERE chat_id = {chat_id}")
      if cursor.fetchone() == None:
        cursor.execute(f"INSERT INTO usuarios(chat_id, saldo, compras, id) VALUES ({chat_id}, 0, 0, DEFAULT)")
        conn.commit()
    except:
        cursor.execute("ROLLBACK")
        conn.commit()
def resgistro(chat_id):
  try:
    sql = f"SELECT data_entrada FROM usuarios WHERE chat_id = {chat_id}"
    cursor.execute(sql)
    for data in cursor.fetchone():
      ...
    return data
  except:
    cursor.execute("ROLLBACK")
    conn.commit()
    
def saldo(chat_id):
  try:
    sql = f"SELECT saldo FROM usuarios WHERE chat_id = {chat_id}"
    cursor.execute(sql)
    for saldo in cursor.fetchone():
      ...
    return saldo
  except:
    cursor.execute("ROLLBACK")
    conn.commit()
def compras(chat_id):
  try:
    sql = f"SELECT compras FROM usuarios WHERE chat_id = {chat_id}"
    cursor.execute(sql)
    for compras in cursor.fetchone():
      ...
    return compras
  except:
    cursor.execute("ROLLBACK")
    conn.commit()
def pesquisar_valores(tipo):
  cursor.execute(f"SELECT valor FROM valores WHERE tipo = '{tipo}'")
  for resultado in cursor.fetchone():
    ...
  return resultado
def email(tipo):
	cursor.execute(f"SELECT email FROM contas WHERE tipo = '{tipo}'")
	r2 = cursor.fetchone()
	for email in r2:
	  ...
	return email
def senha(tipo):
	cursor.execute(f"SELECT senha FROM contas WHERE email = '{email(tipo)}'")
	for us in cursor.fetchone():
	    ...
	return us

def tela(tipo):
	cursor.execute(f"SELECT tela FROM contas WHERE email = '{email(tipo)}'")
	for us in cursor.fetchone():
		...
	return us

def pin(tipo):
	cursor.execute(f"SELECT pin FROM contas WHERE email = '{email(tipo)}'")
	for us in cursor.fetchone():
		...
	return us


def verificar_total(tipo):
  try:
    sql = f"SELECT COUNT(*) FROM contas WHERE tipo = '{tipo}'"
    cursor.execute(sql)
    return cursor.fetchone()
  except:
    cursor.execute("ROLLBACK")
    conn.commit()

def delete_conta(conta):
  sql = f"DELETE FROM contas WHERE email = '{conta}'"
  cursor.execute(sql)
  conn.commit()
  return "APAGADO"
  
def update(saldo, compras, chat_id):
  cursor.execute(f"UPDATE usuarios SET saldo = {saldo}, compras = {compras} WHERE chat_id = {chat_id}")
  conn.commit()
  
def VALOR(tipo):
    s = pesquisar_valores(tipo)
    return s 
