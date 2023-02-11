import time, json, os, requests, random, mercadopago, telebot, uuid
from markups import *
from buscando_dados import *
from gerar_pagamento import *

giftcard = uuid.uuid4()

def gerar_id():
  return random.randint(0, 50000)

def notificar_recarga(id_ta, valor, user):
    bot.send_message(-1001783823529, f"""
    🎁 Recarga Pix realizada

Id da transação: {id_ta}
Valor: R${valor},00
Usuário: {user}

<a href='https://t.me/MdzShopBot'>Recarregue na store!</a>
""", parse_mode="HTML")

def notificar_compra(tipo, valor, user):
    bot.send_message(-1001783823529, f"""
    🎁 Conta Comprada

Conta: {tipo}
Valor: R${valor},00
Usuário: {user}

<a href='https://t.me/MdzShopBot'>Recarregue na store!</a>
""", parse_mode="HTML")

with open('config/config.json', 'r') as file:
        config = json.loads(file.read())
        token = config['token']
bot = telebot.TeleBot(token)
#;
@bot.message_handler(commands=['add2'])
def uploa2d(message):
  lista = message.text.split("/add2 ")[1]
  i = list(enumerate(lista))
  print(i)

@bot.message_handler(commands=['id'])
def id_addss(message):
    if verificar_admin(message.from_user.id) == True:
    	try:
             cursor.execute( f"SELECT saldo FROM usuarios WHERE chat_id = {message.chat.id}")
             if cursor.fetchone() == None:
                   cursor.execute(f"INSERT INTO usuarios(chat_id, saldo, compras, id) VALUES ({message.chat.id}, 0, 0, DEFAULT)")
                   conn.commit()
    	except:
             cursor.execute("ROLLBACK")
             conn.commit()
#k
@bot.message_handler(commands=['add'])
def upload(message):
    if verificar_admin(message.from_user.id) == True:
      bot.send_message(message.chat.id, """
Escolha alguma opção abaixo:

🔹 ADICIONAR SÓ UMA CONTA
🔸 ADICIONAR VÁRIAS CONTAS
""", reply_markup=add_conta)

@bot.message_handler(commands=['price'])
def price(message):
  if verificar_admin(message.from_user.id) == True:
      if message.text == "/price":
          bot.send_message(message.chat.id, """
         * ➕ Mude os valores das contas
          
Modo de uso:* `/price nome da contas|valor que deseja colocar`
          """, parse_mode="MARKDOWN")
      else:
              texto = message.text.split("/price ")[1]
              cont = texto.split("|")[0]
              conta = cont.lower()
              valor = texto.split("|")[1]
              update_valores(conta, int(valor))
              bot.send_message(message.chat.id, "Valor Modificado!")
  else:
      bot.send_message(message.chat.id, "*Você não possui autorização!*", parse_mode="MARKDOWN")
@bot.message_handler(content_types=['photo'])
def photo(message):
  if message.chat.type == "private":
     if verificar_admin(message.from_user.id) == True:
        raw = message.photo[2].file_id
        path = raw+".jpg"
        file_info = bot.get_file(raw)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(path,'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(message.chat.id, """Enviando mensagem 📥
""")
        cursor.execute("SELECT chat_id FROM usuarios")
        captio = message.caption
        for lista in cursor.fetchall():
            for s3 in lista:
                with open(path, "rb") as s2:
                    if captio == None:
                        captio = ""
                        s=requests.post(f"https://api.telegram.org/bot{token}/sendPhoto?chat_id={s3}&caption={captio}", files={'photo': s2})
                    else:
                        s=requests.post(f"https://api.telegram.org/bot{token}/sendPhoto?chat_id={s3}&caption={captio}&parse_mode=MARKDOWN", files={'photo': s2})
 
@bot.message_handler(commands=['admin'])
def admin(message):
  if verificar_admin(message.from_user.id) == True:
      bot.send_message(message.chat.id, """
*⚙️ PAINEL ADMINISTRATIVO*

_• Cmds Admin:_
 
`/add` *- ADICIONAR CONTAS NA STORE*
`/deladmin` *- DELETAR ADMIN*
`/addadmin` *- ADICIONAR ADMIN*
`/send` *- NOTIFICAR USUÁRIOS*
`/gerar` *- GERAR GIFT*
`/dimn` *- DIMINUIR SALDO DE USUÁRIO*
`/price` *- MUDAR VALORES CONTAS*
`/infor` *- MOSTRA INFORMAÇÕES DO USUÁRIO NO BANCO DE DADOS*

*PARA ENVIAR UMA FOTO PARA OS USUÁRIOS DA STORE SÓ PRECISA ENVIAR A FOTO NO PRIVADO DO BOT.*
""", parse_mode="MARKDOWN")
@bot.message_handler(commands=['addadmin'])
def admin(message):
  if verificar_admin(message.from_user.id) == True:
    ID_ADMIN = message.text.split("/addadmin ")[1]
    adicionar_admin(ID_ADMIN)
    bot.send_message(message.chat.id, f"""
    ✅ ADMIN ADICIONADO
    
ᒥ ID ⇒  {ID_ADMIN} 🜲
ᒪ ADICIONADO POR ⇒ {message.from_user.first_name} 🜲
""")
@bot.message_handler(commands=['deladmin'])
def excluir_admin(message):
  if verificar_admin(message.from_user.id) == True:
    try:
        ID_ADMIN = message.text.split("/deladmin ")[1]
        deletar_admin(ID_ADMIN)
        bot.send_message(message.chat.id, f"""
        ✅ ADMIN EXCLUÍDO 
        
ᒥ ID ⇒  {ID_ADMIN} 🜲
ᒪ EXCLUÍDO POR ⇒ {message.from_user.first_name} 🜲
    """)
    except:
        ...
@bot.message_handler(commands=['infor'])
def info(message):
  if verificar_admin(message.from_user.id) == True:
    if message.text == "/infor":
       bot.send_message(message.chat.id, """
         * 👤 Veja as informações
         
Modo de uso:* `/infor id de usuário`
          """, parse_mode="MARKDOWN")
    else:
        chat_id = message.text.split("/infor ")[1]
        verificar_existe(int(chat_id))
        bot.send_message(message.chat.id, f"""
        🔍 *USUÁRIO ENCONTRADO

- ID: {chat_id}
- SALDO: {saldo(int(chat_id))}
- COMPRAS: {compras(int(chat_id))}*
          """, parse_mode="MARKDOWN")
@bot.message_handler(commands=['send'])
def notificar(message):
  if verificar_admin(message.from_user.id) == True:
    if message.text == "/send":
                bot.send_message(message.chat.id, """
                *📣 Envie uma mensagem para todos os usuários registrados no bot.

Ex:* _/send + a mensagem que deseja enviar_
                """, parse_mode="MARKDOWN")
    else:
                MSG = message.text.split("/send ")[1]
                bot.send_message(message.chat.id, "Enviando mensagem 📥")
                cursor.execute("SELECT chat_id FROM usuarios")
                for lista in cursor.fetchall():
                    for s in lista:
                      s=requests.post(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={s}&text={MSG}&parse_mode=MARKDOWN")


@bot.message_handler(commands=['gerar'])
def gerar_gift(message):
  if verificar_admin(message.from_user.id) == True:
            if message.text == "/gerar":
                bot.send_message(message.chat.id, """
                *💵 Gere um gift card para o usuário resgatar.*

*Ex:* `/gerar` _+ valor que deseja adicionar_
                """, parse_mode="MARKDOWN")
            else:
                VALOR = int(message.text.split("/gerar ")[1])
                cursor.execute(f"INSERT INTO gifts_cards(gift_gerado, valor) VALUES('{giftcard}', {VALOR}) RETURNING id;")
                conn.commit()
                bot.send_message(message.chat.id, f"""
             * ✅ GIFT GERADO

GIFT ⇒ *`/resgatar {giftcard}`
*VALOR ⇒* `R${VALOR}`
*𐃘 SÓ PODE UTILIZAR UMA VEZ ESSE CÓDIGO*
""", parse_mode="MARKDOWN")
  else:
      bot.send_message(message.chat.id, "*Você não possui autorização!*", parse_mode="MARKDOWN")
@bot.message_handler(commands=['resgatar'])
def resgatar_gitf(message):
      verificar_existe(message.from_user.id)
      if message.text == "/resgatar":
          bot.send_message(message.chat.id, """
    🏷 *De o comando /resgatar + o gift a ser resgatado.*
    """, parse_mode="MARKDOWN")
      elif message.text == "/resgatar@seubot":
          bot.send_message(message.chat.id, """
    🏷 *De o comando /resgatar + o gift a ser resgatado.*
    """, parse_mode="MARKDOWN")
      else:
          gift_enviado = message.text.split("/resgatar ")[1]
          try:  
              cursor.execute(f"SELECT valor FROM gifts_cards WHERE gift_gerado = '{gift_enviado}'")
              for result in cursor.fetchone():
                  pass
              ADD_SALDO = saldo(message.from_user.id) + result
              cursor.execute(f"UPDATE usuarios SET saldo = {ADD_SALDO} WHERE chat_id = {message.from_user.id}")
              conn.commit()
              bot.send_message(message.chat.id,"❗️*GIFT CARD RESGATADO!!! APROVEITE SEU SALDO E COMPRE NA STORE.*", parse_mode="MARKDOWN")
              cursor.execute(f"DELETE FROM gifts_cards WHERE gift_gerado = '{gift_enviado}'")
              conn.commit()
              bot.send_message(-1001521023988,f"""
  💳 Gift Resgatado

Valor: R${result}
Id: {message.from_user.id}
Usuário: {message.from_user.username}

<a href='https://t.me/urldoseubot'>Recarregue na store!</a>
  """, parse_mode="HTML")
          except:
              bot.send_message(message.chat.id,"❗️*ESSE GIFT CARD É ÍNVALIDO, ADICIONE SALDO NO BOT E PEÇA PARA O DONO GERAR UM GIFT PARA VOCÊ.*", parse_mode="MARKDOWN")

@bot.message_handler(commands=['dimn'])
def diminuir_slo(message):
  if verificar_admin(message.from_user.id) == True:
      if message.text == "/dimn":
          bot.send_message(message.chat.id, """
          *➖ Diminuir saldo

Modo de usar:* `/dimn` *id de usuário|quantidade para diminuir*
   """, parse_mode="MARKDOWN")
      else:
          texto = message.text.split("/dimn ")[1]
          chat = texto.split("|")[0]
          s = texto.split("|")[1]
          s2 = saldo(int(chat)) - int(s)
          diminuir_saldo(int(chat), s2)
          bot.send_message(message.chat.id, "Saldo Diminuído!")
@bot.message_handler(commands=['start'])
def start(message):
  verificar_existe(message.from_user.id) 
  bot.send_message(message.chat.id, "*Olá caro Usuário! Digite o /menu para exibir o menu do bot.*", parse_mode="MARKDOWN")

@bot.message_handler(commands=['menu'])
def menu(message):
	   verificar_existe(message.from_user.id) 
	   cursor.execute("SELECT COUNT(*) FROM usuarios")
	   for total in cursor.fetchone():
	       ...
	   bot.send_message(message.chat.id, f"""
*Olá {message.from_user.first_name}, seja bem vindo(a) a store.

- Total de Usuários no bot:* `{total}`

_➤ Informações:_
 *├ ID:* `{message.from_user.id}`
 *└💰 Saldo:* `R${saldo(message.from_user.id)}`
        """, reply_markup=inicio2, parse_mode="MARKDOWN")

@bot.message_handler(commands=['recarga'])
def recarga_pix(message):
  verificar_existe(message.from_user.id)
  if message.text == "/recarga":
    bot.send_message(message.chat.id, "*Digite /recarga + o valor que deseja.*", parse_mode="MARKDOWN")
  elif message.text == "/recarga@seubot":
    bot.send_message(message.chat.id, "*Digite /recarga + o valor que deseja.*", parse_mode="MARKDOWN")
  else:
    try:
      VALOR = message.text.split("/recarga ")[1]
      id_pix = gerar_pagamento(int(VALOR))[0]
      token = ""
      headers = {"Authorization": f"Bearer {token}"}
      request = requests.get(f'https://api.mercadopago.com/v1/payments/{id_pix}', headers=headers)
      response = request.json()
      pix = response['point_of_interaction']['transaction_data']['qr_code']
      msg = bot.send_message(message.chat.id, f"""
    *✅ PAGAMENTO GERADO

ℹ️  ID DO PAGAMENTO:* `{id_pix}`
*ℹ️  PIX QR CODE:* `{pix}`
*ℹ️  A COMPRA IRÁ EXPIRAR EM 5 MINUTOS.
ℹ️  DEPOIS DO PAGAMENTO SEU SALDO SERÁ ADICIONADO AUTOMÁTICAMENTE.*""",
  reply_markup=aguardando, parse_mode="MARKDOWN")
      if status(id_pix) == True:
        adicao = int(VALOR) + saldo(message.from_user.id)
        sql = f"UPDATE usuarios SET saldo = {adicao} WHERE chat_id = {message.from_user.id}"
        cursor.execute(sql)
        conn.commit()
        bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text="*• PAGAMENTO APROVADO!!! SEU SALDO JA ESTÁ DISPONÍVEL.🤴💰*", parse_mode="MARKDOWN")
        notificar_recarga(id_pix, VALOR, message.from_user.first_name)
      else:
        bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text="*• O PAGAMENTO FOI EXPIRADO.*", parse_mode="MARKDOWN")
    except:
      bot.send_message(message.chat.id,"*• Você digitou o valor incorretamente , use um valor inteiro , exemplo: /recarga 1.*", parse_mode="MARKDOWN")
      
@bot.callback_query_handler(func=lambda call: call.data == "net")
def net_call(call):
  bot.answer_callback_query(callback_query_id=call.id , text="Em manutenção.", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data == "resgatar")
def resgatar(call):
  bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
        🏷 *De o comando /resgatar + o gift a ser resgatado.* 
                """, parse_mode="MARKDOWN", reply_markup=i)
@bot.callback_query_handler(func=lambda call: call.data == "add_1")
def add_i(call):
    if verificar_admin(call.from_user.id) == True:
      msg = bot.send_message(call.message.chat.id, """
Qual conta você deseja adicionar?
""")
      bot.register_next_step_handler(msg, process_addcont)

def process_addcont(message):
  global conta
  conta = message.text.lower()
  if verificar_tipo(conta) == True:
    if conta == "netflix":
        msg = bot.send_message(message.chat.id, "Envie a conta no formato email|senha|tela|pin")
        bot.register_next_step_handler(msg, add_count_m)
    else:
        msg = bot.send_message(message.chat.id, "Envie a conta no formato email|senha.")
        bot.register_next_step_handler(msg, add_count_m)
  else:
    bot.send_message(message.chat.id, "Essa conta não existe, reinicie o processo digitando /add. 🤖")
def add_count_m(message):
  try:
    if conta == "netflix":
        email = message.text.split("|")[0]
        senha = message.text.split("|")[1]
        tela = message.text.split("|")[2]
        pin = message.text.split("|")[3]
        adicionar_conta(conta, email, senha, tela, pin)
        bot.send_message(message.chat.id, f"""
*🔥 CONTA ADICIONADA NO BOT*
    
*📧 EMAIL:* `{email}`
*🔒 SENHA:* `{senha}`
*📱 TELA:* `{tela}`
*🔑 PIN:* `{pin}`
*📥 CONTA:* `{conta}`
    """, parse_mode="MARKDOWN")
    else:
        email = message.text.split("|")[0]
        senha = message.text.split("|")[1]
        tela = "NULL"
        pin = 0
        adicionar_conta(conta, email, senha, tela, pin)
        bot.send_message(message.chat.id, f"""
*🔥 CONTA ADICIONADA NO BOT*
    
*📧 EMAIL:* `{email}`
*🔒 SENHA:* `{senha}`
*📥 CONTA:* `{conta}`
    """, parse_mode="MARKDOWN")
  except:
    bot.send_message(message.chat.id, "Ocorreu um erro inesperado.")

@bot.callback_query_handler(func=lambda call: call.data == "amoporno")
def amoporno(call):
      if int(amoporno_quant()) == 0:
          bot.answer_callback_query(callback_query_id=call.id , text="Não possuimos estoque no momento ou não possuimos todas as contas.", show_alert=True)
      else:
          if saldo(call.from_user.id) >= VALOR('amoporno'):
                        compras_ajustadas = compras(call.from_user.id) + 1
                        saldo_ajustado = saldo(call.from_user.id) - VALOR('amoporno')
                        time.sleep(2)
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
                ✅ *Compra efetuada com sucesso*
    
📧 *E-mail:* `{email('amoporno')}`
🔒 *Senha:* `{senha('amoporno')}`
📥 *Conta:* Amo Porno Br
📆 *Validade:* 30 Dias
🆘 *Suporte:* 24 Horas apartir da compra
⚙️ *Id da compra:* {gerar_id()}
    
❌_Não responsabilizaremos pela perda da conta ou troca de senha. Até porque não trocamos senha de nenhuma conta._
                """, reply_markup=cc_comp(call.from_user.id), parse_mode="MARKDOWN")
                        delete_conta(email('amoporno'))
                        update(saldo_ajustado, compras_ajustadas, call.from_user.id)
                        notificar_compra("Amo Porno Br", VALOR('amoporno'), call.from_user.first_name)
@bot.callback_query_handler(func=lambda call: call.data == "telecine")
def telecine(call):
      if int(telecine_quant()) == 0:
          bot.answer_callback_query(callback_query_id=call.id , text="Não possuimos estoque no momento ou não possuimos todas as contas.", show_alert=True)
      else:
          if saldo(call.from_user.id) >= VALOR('telecine'):
                        compras_ajustadas = compras(call.from_user.id) + 1
                        saldo_ajustado = saldo(call.from_user.id) - VALOR('telecine')
                        time.sleep(2)
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
                ✅ *Compra efetuada com sucesso*
    
📧 *E-mail:* `{email('telecine')}`
🔒 *Senha:* `{senha('telecine')}`
📥 *Conta:* Telecine
📆 *Validade:* 30 Dias
🆘 *Suporte:* 24 Horas apartir da compra
⚙️ *Id da compra:* {gerar_id()}
    
❌_Não responsabilizaremos pela perda da conta ou troca de senha. Até porque não trocamos senha de nenhuma conta._
                """, reply_markup=cc_comp(call.from_user.id),parse_mode="MARKDOWN")
                        delete_conta(email('telecine'))
                        update(saldo_ajustado, compras_ajustadas, call.from_user.id)
                        notificar_compra("Telecine", VALOR('telecine'), call.from_user.first_name)
          else:
                    bot.answer_callback_query(callback_query_id=call.id , text="Você não possui saldo suficiente, recarregue na store.", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data == "tufos")
def tufos(call):
      if int(tufos_quant()) == 0:
          bot.answer_callback_query(callback_query_id=call.id , text="Não possuimos estoque no momento ou não possuimos todas as contas.", show_alert=True)
      else:
          if saldo(call.from_user.id) >= VALOR('tufos'):
                        compras_ajustadas = compras(call.from_user.id) + 1
                        saldo_ajustado = saldo(call.from_user.id) - VALOR('tufos')
                        msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Comprando a conta...")
                        time.sleep(2)
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
                ✅ *Compra efetuada com sucesso*
    
📧 *E-mail:* `{email('tufos')}`
🔒 *Senha:* `{senha('tufos')}`
📥 *Conta:* Tufos
📆 *Validade:* 30 Dias
🆘 *Suporte:* 24 Horas apartir da compra
⚙️ *Id da compra:* {gerar_id()}
    
❌_Não responsabilizaremos pela perda da conta ou troca de senha. Até porque não trocamos senha de nenhuma conta._
                """, reply_markup=cc_comp(call.from_user.id),parse_mode="MARKDOWN")
                        delete_conta(email('tufos'))
                        update(saldo_ajustado, compras_ajustadas, call.from_user.id)
                        notificar_compra("Tufos", VALOR('tufos'), call.from_user.first_name)
          else:
                    bot.answer_callback_query(callback_query_id=call.id , text="Você não possui saldo suficiente, recarregue na store.", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data == "netflix")
def netflix(call):
      if int(netflix_quant()) == 0:
          bot.answer_callback_query(callback_query_id=call.id , text="Não possuimos estoque no momento ou não possuimos todas as contas.", show_alert=True)
      else:
          if saldo(call.from_user.id) >= VALOR('netflix'):
            compras_ajustadas = compras(call.from_user.id) + 1
            saldo_ajustado = saldo(call.from_user.id) - VALOR('netflix')
            time.sleep(2)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
                ✅ *Compra efetuada com sucesso*
    
📧 *E-mail:* `{email('netflix')}`
🔒 *Senha:* `{senha('netflix')}`
📱 *Tela:* `{tela('netflix')}`
🔑 *Pin:* `{pin('netflix')}`
📥 *Conta:* Tela Netflix
📆 *Validade:* 30 Dias
🆘 *Suporte:* 24 Horas apartir da compra
⚙️ *Id da compra:* {gerar_id()}
    
❌_Não responsabilizaremos pela perda da conta ou troca de senha. Até porque não trocamos senha de nenhuma conta._
                """, reply_markup=cc_comp(call.from_user.id),parse_mode="MARKDOWN")
            delete_conta(email('netflix'))
            update(saldo_ajustado, compras_ajustadas, call.from_user.id)
            notificar_compra("Netflix", VALOR('netflix'), call.from_user.first_name)
          else:
            bot.answer_callback_query(callback_query_id=call.id , text="Você não possui saldo suficiente, recarregue na store.", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data == "disney")
def disney(call):
      if int(disney_quant()) == 0:
          bot.answer_callback_query(callback_query_id=call.id , text="Não possuimos estoque no momento ou não possuimos todas as contas.", show_alert=True)
      else:
          if saldo(call.from_user.id) >= VALOR('disney'):
              compras_ajustadas = compras(call.from_user.id) + 1
              saldo_ajustado = saldo(call.from_user.id) - VALOR('disney')
              time.sleep(2)
              bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
                ✅ *Compra efetuada com sucesso*
    
📧 *E-mail:* `{email('disney')}`
🔒 *Senha:* `{senha('disney')}`
📥 *Conta:* Disney Plus
📆 *Validade:* 30 Dias
🆘 *Suporte:* 24 Horas apartir da compra
⚙️ *Id da compra:* {gerar_id()}
    
❌_Não responsabilizaremos pela perda da conta ou troca de senha. Até porque não trocamos senha de nenhuma conta._
    """,reply_markup=cc_comp(call.from_user.id), parse_mode="MARKDOWN")
              delete_conta(email('disney'))
              update(saldo_ajustado, compras_ajustadas, call.from_user.id)
              notificar_compra("Disney Plus", VALOR('disney'), call.from_user.first_name)
          else:
                bot.answer_callback_query(callback_query_id=call.id , text="Você não possui saldo suficiente, recarregue na store.", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data == "primevideo")
def primevideo(call):
      if int(prime_quant()) == 0:
          bot.answer_callback_query(callback_query_id=call.id , text="Não possuimos estoque no momento ou não possuimos todas as contas.", show_alert=True)
      else:
          if saldo(call.from_user.id) >= VALOR('prime'):
              compras_ajustadas = compras(call.from_user.id) + 1
              saldo_ajustado = saldo(call.from_user.id) - VALOR('prime')
              time.sleep(2)
              bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
                ✅ *Compra efetuada com sucesso*
    
📧 *E-mail:* `{email('prime')}`
🔒 *Senha:* `{senha('prime')}`
📥 *Conta:* Prime Vídeo
📆 *Validade:* 30 Dias
🆘 *Suporte:* 24 Horas apartir da compra
⚙️ *Id da compra:* {gerar_id()}
    
❌_Não responsabilizaremos pela perda da conta ou troca de senha. Até porque não trocamos senha de nenhuma conta._
                """, reply_markup=cc_comp(call.from_user.id),parse_mode="MARKDOWN")
              delete_conta(email('prime'))
              update(saldo_ajustado, compras_ajustadas, call.from_user.id)
              notificar_compra("Prime Vídeo", VALOR('prime'), call.from_user.first_name)
          else:
              bot.answer_callback_query(callback_query_id=call.id , text="Você não possui saldo suficiente, recarregue na store.", show_alert=True)
 
@bot.callback_query_handler(func=lambda call: call.data == "globo")
def globo(call):
      if int(globo_quant()) == 0:
          bot.answer_callback_query(callback_query_id=call.id , text="Não possuimos estoque no momento ou não possuimos todas as contas.", show_alert=True)
      else:
          if saldo(call.from_user.id) >= VALOR('globo'):
              compras_ajustadas = compras(call.from_user.id) + 1
              saldo_ajustado = saldo(call.from_user.id) - VALOR('globo')
              time.sleep(2)
              bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
                ✅ *Compra efetuada com sucesso*
    
📧 *E-mail:* `{email('globo')}`
🔒 *Senha:* `{senha('globo')}`
📥 *Conta:* Globo Play
📆 *Validade:* 30 Dias
🆘 *Suporte:* 24 Horas apartir da compra
⚙️ *Id da compra:* {gerar_id()}
    
❌_Não responsabilizaremos pela perda da conta ou troca de senha. Até porque não trocamos senha de nenhuma conta._
            """, reply_markup=cc_comp(call.from_user.id),parse_mode="MARKDOWN")
              delete_conta(email('globo'))
              update(saldo_ajustado, compras_ajustadas, call.from_user.id)
              notificar_compra("Globo Play", VALOR('globo'), call.from_user.first_name)
          else:
              bot.answer_callback_query(callback_query_id=call.id , text="Você não possui saldo suficiente, recarregue na store.", show_alert=True)
@bot.callback_query_handler(func=lambda call: call.data == "spotify")
def spotify(call):
      if int(spotify_quant()) == 0:
          bot.answer_callback_query(callback_query_id=call.id , text="Não possuimos estoque no momento ou não possuimos todas as contas.", show_alert=True)
      else:
          if saldo(call.from_user.id) >= VALOR('spotify'):
              compras_ajustadas = compras(call.from_user.id) + 1
              saldo_ajustado = saldo(call.from_user.id) - VALOR('spotify')
              time.sleep(2)
              bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
                ✅ *Compra efetuada com sucesso*
    
📧 *E-mail:* `{email('spotify')}`
🔒 *Senha:* `{senha('spotify')}`
📥 *Conta:* Spotify Premium
📆 *Validade:* 30 Dias
🆘 *Suporte:* 24 Horas apartir da compra
⚙️ *Id da compra:* {gerar_id()}
    
❌_Não responsabilizaremos pela perda da conta ou troca de senha. Até porque não trocamos senha de nenhuma conta._
            """, reply_markup=cc_comp(call.from_user.id),parse_mode="MARKDOWN")
              delete_conta(email('spotify'))
              update(saldo_ajustado, compras_ajustadas, call.from_user.id)
              notificar_compra("Spotify", VALOR('spotify'), call.from_user.first_name)
          else:
              bot.answer_callback_query(callback_query_id=call.id , text="Você não possui saldo suficiente, recarregue na store.", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data == "hbo")
def hbo(call):
      if int(hbo_quant()) == 0:
          bot.answer_callback_query(callback_query_id=call.id , text="Não possuimos estoque no momento ou não possuimos todas as contas.", show_alert=True)
      else:
          if saldo(call.from_user.id) >= VALOR('hbo'):
              compras_ajustadas = compras(call.from_user.id) + 1
              saldo_ajustado = saldo(call.from_user.id) - VALOR('hbo')
              time.sleep(2)
              bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
                ✅ *Compra efetuada com sucesso*
    
📧 *E-mail:* `{email('hbo')}`
🔒 *Senha:* `{senha('hbo')}`
📥 *Conta:* Hbo Max
📆 *Validade:* 30 Dias
🆘 *Suporte:* 24 Horas apartir da compra
⚙️ *Id da compra:* {gerar_id()}
    
❌_Não responsabilizaremos pela perda da conta ou troca de senha. Até porque não trocamos senha de nenhuma conta._
            """, reply_markup=cc_comp(call.from_user.id),parse_mode="MARKDOWN")
              delete_conta(email('hbo'))
              update(saldo_ajustado, compras_ajustadas, call.from_user.id)
              notificar_compra("Hbo Max", VALOR('hbo'), call.from_user.first_name)
          else:
              bot.answer_callback_query(callback_query_id=call.id , text="Você não possui saldo suficiente, recarregue na store.", show_alert=True)
   
@bot.callback_query_handler(func=lambda call: call.data == "star")
def star(call):
      if int(star_quant()) == 0:
          bot.answer_callback_query(callback_query_id=call.id , text="Não possuimos estoque no momento ou não possuimos todas as contas.", show_alert=True)
      else:
          if saldo(call.from_user.id) >= VALOR('star'):
              compras_ajustadas = compras(call.from_user.id) + 1
              saldo_ajustado = saldo(call.from_user.id) - VALOR('star')
              time.sleep(2)
              bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
                ✅ *Compra efetuada com sucesso*
    
📧 *E-mail:* `{email('star')}`
🔒 *Senha:* `{senha('star')}`
📥 *Conta:* Star Plus
📆 *Validade:* 30 Dias
🆘 *Suporte:* 24 Horas apartir da compra
⚙️ *Id da compra:* {gerar_id()}
    
❌_Não responsabilizaremos pela perda da conta ou troca de senha. Até porque não trocamos senha de nenhuma conta._
                """, reply_markup=cc_comp(call.from_user.id),parse_mode="MARKDOWN")
              delete_conta(email('star'))
              update(saldo_ajustado, compras_ajustadas, call.from_user.id)
              notificar_compra("Star Plus", VALOR('star'), call.from_user.first_name)
          else:
              bot.answer_callback_query(callback_query_id=call.id , text="Você não possui saldo suficiente, recarregue na store.", show_alert=True)
 
@bot.callback_query_handler(func=lambda call: call.data == "youtube")
def youtube(call):
      if int(youtube_quant()) == 0:
          bot.answer_callback_query(callback_query_id=call.id , text="Não possuimos estoque no momento ou não possuimos todas as contas.", show_alert=True)
      else:
          if saldo(call.from_user.id) >= VALOR('youtube'):
              compras_ajustadas = compras(call.from_user.id) + 1
              saldo_ajustado = saldo(call.from_user.id) - VALOR('youtube')
              time.sleep(2)
              bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
                ✅ *Compra efetuada com sucesso*
    
📧 *E-mail:* `{email('youtube')}`
🔒 *Senha:* `{senha('youtube')}`
📥 *Conta:* YouTube Premium
📆 *Validade:* 30 Dias
🆘 *Suporte:* 24 Horas apartir da compra
⚙️ *Id da compra:* {gerar_id()}
    
❌_Não responsabilizaremos pela perda da conta ou troca de senha. Até porque não trocamos senha de nenhuma conta._
                """, reply_markup=cc_comp(call.from_user.id),parse_mode="MARKDOWN")
              delete_conta(email('youtube'))
              update(saldo_ajustado, compras_ajustadas, call.from_user.id)
              notificar_compra("YouTube Premium", VALOR('youtube'), call.from_user.first_name)
          else:
              bot.answer_callback_query(callback_query_id=call.id , text="Você não possui saldo suficiente, recarregue na store.", show_alert=True)
     
@bot.callback_query_handler(func=lambda call: call.data == "tidal")
def tidal(call):
      if int(tidal_quant()) == 0:
          bot.answer_callback_query(callback_query_id=call.id , text="Não possuimos estoque no momento ou não possuimos todas as contas.", show_alert=True)
      else:
          if saldo(call.from_user.id) >= VALOR('tidal'):
              compras_ajustadas = compras(call.from_user.id) + 1
              saldo_ajustado = saldo(call.from_user.id) - VALOR('tidal')
              time.sleep(2)
              bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
                ✅ *Compra efetuada com sucesso*
    
📧 *E-mail:* `{email('tidal')}`
🔒 *Senha:* `{senha('tidal')}`
📥 *Conta:* Tidal Hifi
📆 *Validade:* 30 Dias
🆘 *Suporte:* 24 Horas apartir da compra
⚙️ *Id da compra:* {gerar_id()}
    
❌_Não responsabilizaremos pela perda da conta ou troca de senha. Até porque não trocamos senha de nenhuma conta._
                """, reply_markup=cc_comp(call.from_user.id),parse_mode="MARKDOWN")
              delete_conta(email('tidal'))
              update(saldo_ajustado, compras_ajustadas, call.from_user.id)
              notificar_compra("Tidal Hifi", VALOR('tidal'), call.from_user.first_name)
          else:
              bot.answer_callback_query(callback_query_id=call.id , text="Você não possui saldo suficiente, recarregue na store.", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data == "crunchyroll")
def crunchyroll(call):
      if int(crunchyroll_quant()) == 0:
          bot.answer_callback_query(callback_query_id=call.id , text="Não possuimos estoque no momento ou não possuimos todas as contas.", show_alert=True)
      else:
          if saldo(call.from_user.id) >= VALOR('crunchyroll'):
              compras_ajustadas = compras(call.from_user.id) + 1
              saldo_ajustado = saldo(call.from_user.id) - VALOR('crunchyroll')
              time.sleep(2)
              bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
                ✅ *Compra efetuada com sucesso*
    
📧 *E-mail:* `{email('crunchyroll')}`
🔒 *Senha:* `{senha('crunchyroll')}`
📥 *Conta:* Crunchyroll
📆 *Validade:* 30 Dias
🆘 *Suporte:* 24 Horas apartir da compra
⚙️ *Id da compra:* {gerar_id()}
    
❌_Não responsabilizaremos pela perda da conta ou troca de senha. Até porque não trocamos senha de nenhuma conta._
                """, reply_markup=cc_comp(call.from_user.id),parse_mode="MARKDOWN")
              delete_conta(email('crunchyroll'))
              update(saldo_ajustado, compras_ajustadas, call.from_user.id)
              notificar_compra("Crunchyroll", VALOR('crunchyroll'), call.from_user.first_name)
          else:
              bot.answer_callback_query(callback_query_id=call.id , text="Você não possui saldo suficiente, recarregue na store.", show_alert=True)
      
@bot.callback_query_handler(func=lambda call: call.data == "comprar")
def comprar(call):
  cursor.execute("SELECT COUNT(*) FROM contas")
  for total in cursor.fetchone():
      ...
  bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""*Informações:

- Saldo: R${saldo(call.from_user.id)}
- Contas: {total}

Escolha a opção desejada no menu abaixo.*""", reply_markup=comprar2, parse_mode="MARKDOWN")
@bot.callback_query_handler(func=lambda call: call.data == "back_comprar")
def back_comprar(call):
  cursor.execute("SELECT COUNT(*) FROM usuarios")
  for total in cursor.fetchone():
      ...
  bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
*Olá {call.from_user.first_name}, seja bem vindo(a) a store.

- Total de Usuários no bot:* `{total}`

_➤ Informações:_
 *├ ID:* `{call.from_user.id}`
 *└💰 Saldo:* `R${saldo(call.from_user.id)}`
        """, reply_markup=inicio2, parse_mode="MARKDOWN")
@bot.callback_query_handler(func=lambda call: call.data == "contas_premium")
def conta_premium(call):
        cursor.execute("SELECT COUNT(*) FROM contas")
        for total in cursor.fetchone():
            ...
        if int(total) == 0:
        	 bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
	❌ Não possuimos contas no momento! Volte mais tarde.k
	 """, parse_mode="MARKDOWN",reply_markup=i2)
        else:
	        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
	Escolha uma categoria abaixo
	 """, parse_mode="MARKDOWN",reply_markup=conta_premium2)
@bot.callback_query_handler(func=lambda call: call.data == "recarregar")
def recarregar(call):
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="""
💵 _Adição de Saldo_
    
*• Modo de Usar:*
*Digite o comando* /recarga *+ o valor que deseja adicionar*

*Pode ser qualquer valor! Caso aconteça algum erro fale com o dono*""", parse_mode="MARKDOWN",reply_markup=i)
@bot.callback_query_handler(func=lambda call: call.data == "informacion")
def informacion(call):
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
            📃 *Informações

Perfil ➺
✦ ID: {call.from_user.id}
✦ USUÁRIO: @{call.from_user.username}
✦ DATA ATUAL E HORÁRIO: {day_atual()}

✅ DEV: @gringomdz

Carteira ➺
✦ SALDO: R${saldo(call.from_user.id)}
✦ COMPRAS: {compras(call.from_user.id)}
✦ RESGISTRADO EM: {resgistro(call.from_user.id)}
*
        """, parse_mode="MARKDOWN", reply_markup=i)

@bot.callback_query_handler(func=lambda call: call.data == "conteudo+18")
def musicas_category(call):
            bot.answer_callback_query(callback_query_id=call.id , text="Você escolheu a categoria Conteudo +18!")
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
*🎁 Conta | Preço*

*- Tufos:* `R${VALOR('tufos')},00`
*- Amo Porno Br:* `R${VALOR('amoporno')},00`

⚠️  *Avisos*

_Todas as contas foram testadas e possui validade de 30 dias._
        """, parse_mode="MARKDOWN", reply_markup=conteudo18)

@bot.callback_query_handler(func=lambda call: call.data == "musicas")
def musicas_category(call):
            bot.answer_callback_query(callback_query_id=call.id , text="Você escolheu a categoria Musica!")
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
*🎁 Conta | Preço*

*- Tidal Hifi:* `R${VALOR('tidal')},00`
*- Spotify:* `R${VALOR('spotify')},00`

⚠️  *Avisos*

_Todas as contas foram testadas e possui validade de 30 dias._
        """, parse_mode="MARKDOWN", reply_markup=musicas)

@bot.callback_query_handler(func=lambda call: call.data == "filmeseseries")
def filmeseseries_category(call):
            bot.answer_callback_query(callback_query_id=call.id , text="Você escolheu a categoria Filmes e Series!")
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"""
*🎁 Conta | Preço*

*- Tela Netflix:* `R${VALOR('netflix')},00`
*- Telecine:* `R${VALOR('telecine')},00`
*- Disney Plus:* `R${VALOR('disney')},00`
*- Prime Vídeo:* `R${VALOR('prime')},00`
*- Globo Play:* `R${VALOR('globo')},00`
*- Star Plus:* `R${VALOR('star')},00`
*- YouTube Premium:* `R${VALOR('youtube')},00`
*- Crunchyroll:* `R${VALOR('crunchyroll')},00`
*- Hbo Max:* `R${VALOR('hbo')},00`

⚠️  *Avisos*

_Todas as contas foram testadas e possui validade de 30 dias._
        """, parse_mode="MARKDOWN", reply_markup=filmes)

bot.infinity_polling()