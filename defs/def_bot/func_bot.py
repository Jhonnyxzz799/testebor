import requests
import json
import threading
import arq
import time
import r_texto
import ca
import db
import asyncio
import func
from aiogram.types import InlineQueryResultArticle,InputTextMessageContent
import urllib.parse

dono = arq.ler_json(ca.config)['dono']
dados = arq.ler_json(ca.config)['dados']

ok = '✅'
x = '❌'
voltar = '🔙'


id_dono = dono['id_dono']
suporte = dono['suporte']
id_log = dono['logger']
id_grupo_principal = dono["grupo"]
user_store = (dono['user_store'])
url_store = (dono['user_store']).replace("@","https://t.me/")

# TESTE
token_bot = dono['token_teste']

# BOT
#token_bot = dono['token_bot']

dono = dono['dono']


def send_bot(id, msg,bt=None, parse_mode=None):
    msg = urllib.parse.quote_plus(msg)
    
    if bt != None:
        try:
            bt = json.dumps(bt, indent = 4) 
        except:
            bt = None
            
        
    url = [f'https://api.telegram.org/bot{token_bot}/sendMessage?chat_id={id}&text={msg}']
 
 
    if parse_mode != None:
        url.append('&parse_mode=MarkDownV2')
    
    if bt != None:
        url.append(f"&reply_markup={bt}")

    url = "".join(url)
    
    r = requests.get(url)
    
    return r.text

def send_photo(id, foto, msg=None, bt=None, parse_mode=None):
        if msg!= None:
            msg = urllib.parse.quote_plus(msg)
        
        try:
                
            bt = json.dumps(bt, indent = 4) 
            
        except:
            bt = None


        url = [f'https://api.telegram.org/bot{token_bot}/sendPhoto?chat_id={id}&photo={foto}']
 
 
        if msg != None and msg != 'null':
                url.append(f'&caption={msg}') 
                
        if parse_mode != None and parse_mode != 'null':
                url.append('&parse_mode=MarkDownV2')
            
        if bt != None and bt != 'null':
                url.append(f"&reply_markup={bt}")


        url = "".join(url)

        r = requests.get(url)
        return r.text
    
def edit(id, message_id, msg, bt=None, parse_mode=None):
    msg = urllib.parse.quote_plus(msg)
    
    if bt != None:
        try:
                
            bt = json.dumps(bt, indent = 4) 
            
        except:
            bt = None
            
    
    url = [f"https://api.telegram.org/bot{token_bot}/editMessageText?chat_id={id}&message_id={message_id}&text={msg}"]

    if parse_mode != None:
        url.append('&parse_mode=MarkDownV2')
    
    if bt != None:
        url.append(f"&reply_markup={bt}")

    url = "".join(url)
    
    r = requests.get(url)
    
    return r.text

def send_log(id, msg):
    
    usuario = db.cliente(id)
    
    link = f"[{r_texto.form(usuario['user'])}](tg://user?id={id})"
    
    linhha = f"`{id}` \- {r_texto.form(usuario['nome'])} \- {link}\n{msg}"
    
    return send_bot(id_log, linhha, None, 'mark')


def bt_unitaria():
    precos = arq.ler_json(ca.precos)
    disponiveis = arq.ler_json(ca.quantidade)
    
    bt = {
        "inline_keyboard": ''
        }
    
    cont = 0
    temp = []
    numero = 0
    
    for k,v in precos.items():
        if k in disponiveis and disponiveis[k] > 0:
            nome_bt = f"R${precos[k]} {k} | {disponiveis[k]}"
            
            if int(cont)%2==0:
                temp.append([{"text": nome_bt, "callback_data": k}])
                cont = cont + 0.5
            else:
                temp[numero].append({"text": nome_bt, "callback_data": k})
                cont = cont + 0.5
                numero = numero +1
            
    temp.append([{"text": voltar, "callback_data": "comprar"}])
    bt['inline_keyboard']=temp

    return json.dumps(bt, indent = 4)

def bt_mix():
    mix = arq.ler_json(ca.mix)
    database = db.ccs_json()
    bt = {
        "inline_keyboard": ''
        }
    
    cont = 0
    temp = []
    numero = 0
    
    for k,v in mix.items():
        if int(k) < len(database):
            nome_bt = f"R${v} | {k} CC's"
            
            if int(cont)%2==0:
                temp.append([{"text": nome_bt, "callback_data": k}])
                cont = cont + 0.5
            else:
                temp[numero].append({"text": nome_bt, "callback_data": k})
                cont = cont + 0.5
                numero = numero +1
            
    temp.append([{"text": voltar, "callback_data": "comprar"}])
    bt['inline_keyboard']=temp

    return json.dumps(bt, indent = 4)

def key_ccs():
    
    database = db.ccs_json()
    
    lista = []
    
    for k,v in database.items():
        lista.append(k)

    return lista


def bancos():
    database = db.ccs_json()
    
    lista = []
    
    for k,v in database.items():
        if v['banco'] not in lista:
            lista.append(v['banco'])

    return lista

def bins():
    database = db.ccs_json()
    
    lista = []
    
    for k,v in database.items():
        if v['banco'] not in lista:
            lista.append(v['bin'])

    return lista

    
def art_bank(banco):
    db_cc = db.ccs_json()
    
    banco = banco.split(' ')[1:]
    
    banco = (" ".join(banco)).upper()
    precos = arq.ler_json(ca.precos)

    bt = {
        "inline_keyboard": [
                    
            [{"text": f"Comprar", "callback_data": "comrar_banco_bin_bandeira_tipo"},
            {"text": "Escolher outra", "callback_data": "apagar_inline"}]

            ]
        }

    c = 1
    r = []
    for k,v in db_cc.items():
        cc = v['cc_chk']
        
        if banco in v['banco']:
            
            level = v['level']
            if level in precos:
                preco = precos[level]
                
            else:
                preco = 25
                
            texto = (
                f"💳 Compra por Banco\n\n"
                f"📤 Opção: {v['banco'].title()}\n\n"
                f"📤 Level: {level.title()}\n\n"
                f"📤 Preço: R${preco}\n\n"
            )
            

            val = f"{v['mes']}/{v['ano']}"
            
            desc = (
                f"Bin {k[:6]}\n"
                f"Level {level.title()}\n"
                f"Validade {val}"
            )

            article = InlineQueryResultArticle(
                
                
                
                # The id of our inline result
                id=k,
                title=f"R${preco} - {v['banco']}",
                description = desc,
                thumb_width=5,
                thumb_height=5,
                reply_markup=bt,
                thumb_url="https://cdn-icons-png.flaticon.com/512/147/147258.png",
                input_message_content=InputTextMessageContent(
                    texto
                    )
            )
            
            r.append(article)
            c = c+1
            
            if c > 50:
                break
        
    if len(r) < 1:
        return [
            InlineQueryResultArticle(
                # The id of our inline result
                id=0,
                title=f"❌ Nenhuma cc deste banco foi encontrada!",
                description = (
                    f"Escolha outro banco"
                    ),
                thumb_width=5,
                thumb_height=5,
                input_message_content=InputTextMessageContent('❌ Nenhuma cc deste banco foi encontrada!')
            )
        ]
    else:
        
        
        return r

def art_bin(bin):
    bin = bin.split(' ')[1:]
    bin = " ".join(bin)
    db_cc = db.ccs_json()
    precos = arq.ler_json(ca.precos)
    c = 1
    r = []

    bt = {
        "inline_keyboard": [
                    
            [{"text": f"Comprar", "callback_data": "comrar_banco_bin_bandeira_tipo"},
            {"text": "Escolher outra", "callback_data": "apagar_inline"}]

            ]
        }

    for k,v in db_cc.items():
        cc = v['cc_chk']
        
        if bin in k[:6]:
            
            level = v['level']
            if level in precos:
                preco = precos[level]
                
            else:
                preco = 25
                
            texto = (
                f"💳 Compra por Bin\n\n"
                f"📤 Opção: {v['cc'][:6]}\n\n"
                f"📤 Level: {level.title()}\n\n"
                f"📤 Preço: R${preco}\n\n"
            )
            
            val = f"{v['mes']}/{v['ano']}"
            
            desc = (
                f"Bin {k[:6]}\n"
                f"Level {level.title()}\n"
                f"Validade {val}"
            )

            article = InlineQueryResultArticle(
                
                # The id of our inline result
                id=k,
                title=f"R${preco} - {k[:6]} - {v['banco']}",
                description = desc,
                thumb_width=5,
                thumb_height=5,
                reply_markup=bt,
                thumb_url="https://cdn-icons-png.flaticon.com/512/147/147258.png",
                input_message_content=InputTextMessageContent(
                    texto
                    )
            )
            
            r.append(article)
            c = c+1
            
            if c > 50:
                break
        
    if len(r) < 1:
        return [
            InlineQueryResultArticle(
                # The id of our inline result
                id=0,
                title=f"❌ Nenhuma cc com está bin foi encontrada!",
                description = (
                    f"Digite outra bin"
                    ),
                thumb_width=5,
                thumb_height=5,
                input_message_content=InputTextMessageContent('❌ Nenhuma cc com está bin foi encontrada!')
            )
        ]
    else:
        
        
        return r

def art_bandeira(bandeira):
    
    bandeira = bandeira.split(' ')[1:]
    bandeira = " ".join(bandeira)
    db_cc = db.ccs_json()
    precos = arq.ler_json(ca.precos)
    c = 1
    r = []

    bt = {
        "inline_keyboard": [
                    
            [{"text": f"Comprar", "callback_data": "comrar_banco_bin_bandeira_tipo"},
            {"text": "Escolher outra", "callback_data": "apagar_inline"}]

            ]
        }

    for k,v in db_cc.items():
        cc = v['cc_chk']
        
        if bandeira in v['bandeira'] and v['bandeira'] != 'INDEFINIDO':
            
            level = v['level']
            if level in precos:
                preco = precos[level]
                
            else:
                preco = 25
                
            texto = (
                f"💳 Compra por Bandeira\n\n"
                f"📤 Opção: {v['bandeira'].title()}\n\n"
                f"📤 Level: {level.title()}\n\n"
                f"📤 Preço: R${preco}\n\n"
            )
            
            val = f"{v['mes']}/{v['ano']}"
            
            desc = (
                f"Level {level.title()}\n"
            )

            article = InlineQueryResultArticle(
                
                # The id of our inline result
                id=k,
                title=f"R${preco} - {v['bandeira']}",
                description = desc,
                thumb_width=5,
                thumb_height=5,
                reply_markup=bt,
                thumb_url="https://cdn-icons-png.flaticon.com/512/147/147258.png",
                input_message_content=InputTextMessageContent(
                    texto
                    )
            )
            
            r.append(article)
            c = c+1
            
            if c > 50:
                break
        
    if len(r) < 1:
        return [
            InlineQueryResultArticle(
                # The id of our inline result
                id=0,
                title=f"❌ Nenhuma cc com esta bandeira foi encontrada!",
                description = (
                    f"Escolha outra bandeira"
                    ),
                thumb_width=5,
                thumb_height=5,
                input_message_content=InputTextMessageContent('❌ Nenhuma cc com esta bandeira foi encontrada!')
            )
        ]
    else:
        
        
        return r


def art_tipo(tipo):
    #['DEBITO', 'CREDITO', '', 'MULTIPLO']
    
    tipo = tipo.split(' ')[1:]
    tipo = " ".join(tipo)
    precos = arq.ler_json(ca.precos)
    c = 1
    r = []

    bt = {
        "inline_keyboard": [
                    
            [{"text": f"Comprar", "callback_data": "comrar_banco_bin_bandeira_tipo"},
            {"text": "Escolher outra", "callback_data": "apagar_inline"}]

            ]
        }

    db_cc = db.ccs_json()
    for k,v in db_cc.items():
        cc = v['cc_chk']
        
        if tipo in v['tipo'] and v['tipo'] != 'INDEFINIDO':
            
            level = v['level']
            if level in precos:
                preco = precos[level]
                
            else:
                preco = 25
                
            texto = (
                f"💳 Compra por tipo\n\n"
                f"📤 Opção: {v['tipo'].title()}\n\n"
                f"📤 Level: {level.title()}\n\n"
                f"📤 Preço: R${preco}\n\n"
            )
            
            val = f"{v['mes']}/{v['ano']}"
            
            desc = (
                #f"Bin {k[:6]}\n"
                f"Level {level.title()}\n"
                #f"Validade {val}"
            )

            article = InlineQueryResultArticle(
                
                # The id of our inline result
                id=k,
                title=f"R${preco} - {v['tipo']}",
                description = desc,
                thumb_width=5,
                thumb_height=5,
                reply_markup=bt,
                thumb_url="https://cdn-icons-png.flaticon.com/512/147/147258.png",
                input_message_content=InputTextMessageContent(
                    texto
                    )
            )
            
            r.append(article)
            c = c+1
            
            if c > 50:
                break
        
    if len(r) < 1:
        return [
            InlineQueryResultArticle(
                # The id of our inline result
                id=0,
                title=f"❌ Nenhuma cc com este tipo foi encontrada!",
                description = (
                    f"Escolha outro tipo"
                    ),
                thumb_width=5,
                thumb_height=5,
                input_message_content=InputTextMessageContent('❌ Nenhuma cc com este tipo foi encontrada!')
            )
        ]
    else:
        
        
        return r


async def sender():
    
    if True:
        dados = arq.ler_json(ca.config)['dados']
        clientes = db.id_clientes()
        bt_menu = {
            "inline_keyboard": [
                
                    [{"text": "Menu", "callback_data": "menu"}],
            
                ]
            }

        contador2 = 1

        if dados['sender'] == 'ON':
                enviados = []

                start = int(time.time())

                # ENVIA PARA OS GRUPOS
                spam = arq.ler_json(ca.config)['dono']['spam']

                for c in range(0,len(spam)):
                        #só texto
                        if dados['photo'] == "OFF" and dados['text'] != 'OFF':
                            threading.Thread(target=send_bot,args=(spam[c], dados['text'],)).start()

                        #só foto 
                        if dados['photo'] != "OFF" and dados['text'] == 'OFF':
                            threading.Thread(target=send_photo,args=(spam[c], dados['photo'],)).start()
                            
                        #texto com foto
                        if dados['photo'] != "OFF" and dados['text'] != 'OFF':
                            threading.Thread(target=send_photo,args=(spam[c], dados['photo'], dados['text'],)).start()


                # ENVIA PARA OS USUÁRIOS

                for c in range(0,len(clientes)):
                    time.sleep(0.01)
                    #ENVIAR PARA O DONO
                    if c == 0:
                        send_bot(id_dono, f"🔄 Enviando {c+1} de {len(clientes)} menssagens", None, None)
                    id = clientes[c]


                    if id not in enviados:
                        enviados.append(id)
                        print(f"\r{c}/{len(clientes)} ID {id}",end=" ", flush= True)
                        #só texto
                        if dados['photo'] == "OFF" and dados['text'] != 'OFF':
                            threading.Thread(target=send_bot,args=(id, dados['text'], bt_menu,)).start()

                        #só foto 
                        if dados['photo'] != "OFF" and dados['text'] == 'OFF':
                            threading.Thread(target=send_photo,args=(id, dados['photo'],)).start()
                            
                        #texto com foto
                        if dados['photo'] != "OFF" and dados['text'] != 'OFF':
                            threading.Thread(target=send_photo,args=(id, dados['photo'], dados['text'],)).start()

                        if c >= contador2:
                            texto = f"🔄 Enviando {c} de {len(clientes)} menssagens\n\n🔄 Duração: {int(time.time()-start)} Segundos"

                            contador2 = contador2 + 91

                            threading.Thread(target=edit,args=(id_dono, dados['id'], texto,)).start()
            
                time.sleep(2)
                edit(id_dono, dados['id'], f"✅ Menssagem enviada para {len(clientes)} usuários\n\n✅ Duração: {int(time.time()-start)} Segundos", None, None)

                dados['sender'] = "OFF"
                dados['photo'] = "OFF"
                dados['text'] = "OFF"
                dados['id'] = "OFF"
                
                arq.att_json(ca.config, dados, 1, 'dados')
                
                print('\nMENSSAGEM ENVIADA')
                
        else:
            time.sleep(1)


def enviar():
    threading.Thread(target=asyncio.run, args=(sender(),)).start()

