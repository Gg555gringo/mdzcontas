from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from buscando_dados import *
from telebot.types import InlineKeyboardMarkup,InlineKeyboardButton
aguardando = InlineKeyboardMarkup()
aguardando.row_width = 2
aguardando.add(InlineKeyboardButton("🔁 AGUARDANDO PAGAMENTO", callback_data="."))

inicio2 = InlineKeyboardMarkup()
inicio2.row_width = 1
inicio2.add(InlineKeyboardButton('🛒 Comprar', callback_data='comprar'))
inicio2.row_width = 2
inicio2.add(
    InlineKeyboardButton('💰 Recarregar Saldo', callback_data='recarregar'),
    InlineKeyboardButton('📄 Informações', callback_data='informacion'),
    InlineKeyboardButton('🏷️ Resgatar Gift', callback_data='resgatar'),
    InlineKeyboardButton('❔ Suporte', url='https://t.me/gringomdz'))
inicio2.row_width = 1
inicio2.add(InlineKeyboardButton('👥 Grupo', url='https://t.me/pratest21'))

musicas = InlineKeyboardMarkup()
musicas.row_width = 1
musicas.add(
    InlineKeyboardButton(f'Spotify', callback_data='spotify'),
    InlineKeyboardButton(f'Tidal Hifi', callback_data='tidal'),
    InlineKeyboardButton('🔙 Voltar', callback_data='contas_premium')
    )

conteudo18 = InlineKeyboardMarkup()
conteudo18.row_width = 1
conteudo18.add(
    InlineKeyboardButton('Tufos', callback_data='tufos'),
    InlineKeyboardButton(f'Amo Porno Br', callback_data='amoporno'),
    InlineKeyboardButton('🔙 Voltar', callback_data='contas_premium')
    )

filmes = InlineKeyboardMarkup()
filmes.row_width = 2
filmes.add(
    InlineKeyboardButton(f'Tela Netflix', callback_data='netflix'),
            InlineKeyboardButton(f'Telecine', callback_data='telecine'),
            InlineKeyboardButton(f'Disney Plus', callback_data='disney'),
            InlineKeyboardButton(f'Prime Vídeo', callback_data='primevideo'),
            InlineKeyboardButton(f'Globo play', callback_data='globo'),
            InlineKeyboardButton(f'Star Plus', callback_data='star'),
            InlineKeyboardButton(f'Youtube Premium', callback_data='youtube'),
            InlineKeyboardButton(f'Crunchyroll', callback_data='crunchyroll'),
            InlineKeyboardButton(f'Hbo Max', callback_data='hbo'),
    InlineKeyboardButton('🔙 Voltar', callback_data='contas_premium')
    )

add_conta = InlineKeyboardMarkup()
add_conta.row_width = 1
add_conta.add(
    InlineKeyboardButton('🔹', callback_data='add_1'),InlineKeyboardButton('🔸', callback_data='add_2'))

i2 = InlineKeyboardMarkup()
i2.row_width = 1
i2.add(
    InlineKeyboardButton('🔙 Voltar', callback_data='comprar'))

def cc_comp(id_user):
	u = InlineKeyboardMarkup()
	u.row_width = 1
	u.add(
    InlineKeyboardButton('☑️ Menu Inicial', url=f'https://t.me/MdzShopBot?start={id_user}'))
	return u

i = InlineKeyboardMarkup()
i.row_width = 1
i.add(
    InlineKeyboardButton('🔙 Voltar', callback_data='back_comprar'))

def pesquisar_contas():
    cursor.execute("SELECT tipo FROM contas")
    if cursor.fetchone() == None:
        return None
    else:
        contas = sorted(set(cursor.fetchall()))
        for c in contas:
            print(c)
print(pesquisar_contas())
        
comprar2 = InlineKeyboardMarkup()
comprar2.row_width = 1
comprar2.add(
    InlineKeyboardButton('🍿 Contas Premium', callback_data='contas_premium'),
    InlineKeyboardButton('📱 Net Ilimitada', callback_data='net'),
    InlineKeyboardButton('🔙 Voltar', callback_data='back_comprar'))
 
def telecine_quant():
  for telecine_quant in verificar_total('telecine'):
    ...
  return telecine_quant
def netflix_quant():
  for netflix_quant in verificar_total('netflix'):
    ...
  return netflix_quant
def disney_quant():
  for disney_quant in verificar_total('disney'):
    ...
  return disney_quant
def prime_quant():
  for prime_quant in verificar_total('prime'):
    ...
  return prime_quant
def youtube_quant():
  for youtube_quant in verificar_total('youtube'):
    ...
  return youtube_quant
def star_quant():
  for star_quant in verificar_total('star'):
    ...
  return star_quant
def globo_quant():
  for globo_quant in verificar_total('globo'):
    ...
  return globo_quant
def tidal_quant():
  for tidal_quant in verificar_total('tidal'):
    ...
  return tidal_quant
def hbo_quant():
  for hbo_quant in verificar_total('hbo'):
    ...
  return hbo_quant
def spotify_quant():
  for spotify_quant in verificar_total('spotify'):
    ...
  return spotify_quant
def crunchyroll_quant():
  for crunchyroll_quant in verificar_total('crunchyroll'):
    ...
  return crunchyroll_quant
def tufos_quant():
  for tufos_quant in verificar_total('tufos'):
    ...
  return tufos_quant
  
def amoporno_quant():
  for tufos_quant in verificar_total('amoporno'):
    ...
  return tufos_quant
#is 
conta_premium2 = InlineKeyboardMarkup()
conta_premium2.row_width = 2
conta_premium2.add(InlineKeyboardButton(f'💿 Filmes e Series', callback_data='filmeseseries'),
            InlineKeyboardButton(f'🔥 Conteudo +18', callback_data='conteudo+18'),
            InlineKeyboardButton(f'🎶 Musicas', callback_data='musicas'))
conta_premium2.row_width = 1
conta_premium2.add(InlineKeyboardButton('🔙 Voltar', callback_data='comprar'))
# kk