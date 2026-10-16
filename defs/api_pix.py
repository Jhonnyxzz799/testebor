from sqlite3 import paramstyle
from urllib import response
import requests
import mercadopago
import json
import arq
import func
from def_bot import func_bot
import ca 
import db
import r_texto
import qrcode
from threading import Thread as th
from PIL import Image

from datetime import datetime
import time


def criar_qr_code(id, codigo):
    face = Image.open('./perfil.jpg')

    width, height = face.size

    new_image = face.resize((160, 160))

    qr_big = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )
    qr_big.add_data(codigo)
    qr_big.make()
    img_qr_big = qr_big.make_image().convert('RGB')

    pos = ((img_qr_big.size[0] - new_image.size[0]) // 2, (img_qr_big.size[1] - new_image.size[1]) // 2)

    img_qr_big.paste(new_image, pos)

    img_qr_big.save(f'qr_{id}.jpg')


def criar_pix(id, valor):
      
    minutos = 20
    minutos = minutos * 60
    

    '''apirest = {
                        "status": True,
                        "id_telegram": id,
                        "valor": valor,
                        "id_pagamento": '1234567897',
                        "pix":f'`4648989489498489484`',
                        "qr_code": f"qr_{id}.jpg",
                        "expiracao": (int(time.time()) + minutos),
                        }
    
    return apirest'''

    ret = func.verefica_ban(id)
    if ret == False:
            
        cliente = db.cliente(id)
        
        if cliente['autorizacao'] == False:
            apirest = {
                    "status": False,
                    "message":f'Você foi banido',
                }
            
            return apirest
        
        token_pix = arq.ler_json(ca.config)['dono']["token_pix"]
        
        email = f"{id}@gmail.com"
            
        payment_data = {
                "transaction_amount": valor,
                "description": f"Retorno R${valor} - {id}",
                "payment_method_id": "pix",
                "payer": {
                    "email": email,
                    "first_name": f"{id}",
                    "last_name": f"{id}",
                    }
            }

        payment_response = mercadopago.SDK(token_pix).payment().create(payment_data)
        retorno = payment_response["response"]
            
        
        try:
                id_pagamento = retorno['id']
                valor = retorno['transaction_amount']
                pix = retorno['point_of_interaction']['transaction_data']['qr_code']
                
                qr_code = f'https://chart.apis.google.com/chart?cht=qr&chl={pix}&chs=300x300'
                
                apirest = {
                        "status": True,
                        "id_telegram": id,
                        "valor": valor,
                        "id_pagamento": id_pagamento,
                        "pix":f'`{pix}`',
                        "qr_code": qr_code,
                        "expiracao": (int(time.time()) + minutos),
                        }

                criar_qr_code(id, pix)
                
                    
                arq.att_json(ca.pagamentos, apirest, 1, id_pagamento)
                
                cliente['ban'] = cliente['ban']+1
                
                db.atualiza_cadastro(cliente)
                
                func_bot.send_log(id,f'💠 Pix R${valor} Gerado')
                
                return apirest

        except:
            apirest = {
                    "status": False,
                    "message":f'Token Mercado com problema',
                }
            
            return apirest
        
    else:
        return {
            "status": False,
            "message": f"Você foi banido {ret['message']}"
            }

def retorno_id(id_pagamento):
    '''return {
        "status": True,
        "id": id_pagamento
        }'''
        
    token_pix = arq.ler_json(ca.config)['dono']["token_pix"]
    
    if len(token_pix) != '':
    
        headers = {
            'Authorization': f'Bearer {token_pix}',
        }

        
        try:
            response = requests.get(f'https://api.mercadopago.com/v1/payments/{id_pagamento}', headers=headers)

            retorno = json.loads(response.text)
            
            id_pagamento = retorno['transaction_details']['bank_transfer_id']
            id_transacao = retorno['transaction_details']['transaction_id']
            
            if id_pagamento and id_transacao != None:
                
                return {
                    "status": True,
                    "id": id_pagamento
                    }
                
            else:
                return {
                    "status": "PENDENTE",
                    }
                
        except:
            return {
                    "status": "ERRO",
                    }
    else:
        return {
            "status": "TOKEN DO PIX NÃO DEFINIDO",
            }

           
def adiciona_saldo():
    while True:
        time.sleep(1)
        if len(arq.ler_json(ca.pagamentos)) > 0:
            for k,v in arq.ler_json(ca.pagamentos).items():
                rest = retorno_id(k)
                if rest['status'] == True:
                                        
                    id = v['id_telegram']
                    
                    cliente = db.cliente(id)
                    adicionado = v['valor']
                                                
                    saldo_antigo = cliente['saldo']
                        
                    #adiciona o valor em entrada extrato
                    func.adc_extrato(int(adicionado), 'entrada_pix_rs')

                    if arq.ler_json(ca.config)['dados']['saldo em dobro'] == "ON":
                        adicionado = adicionado * 2
                    
                    novo_saldo = saldo_antigo + adicionado

                    print(novo_saldo)
                    
                    cliente['saldo'] = novo_saldo
                    
                    arq.del_json(ca.pagamentos, 1, str(k))
                    cliente['ban'] = 0
                    db.atualiza_cadastro(cliente)
                    


                    bt = {
                                "inline_keyboard": [
                                    [{"text": f"Menu", "callback_data": "menu"}],
                                    ]
                                }
                    
                    th(target=func_bot.send_bot, args=(id, f"{func_bot.ok} R${adicionado} Adicionado\n\n💵 Novo saldo R${novo_saldo}", bt,)).start()
                    th(target=func_bot.send_log, args=(id, f"💵 R${adicionado} Adicionado \- Novo saldo R${novo_saldo}",)).start()

                    '''link =  f"[{r_texto.form(cliente['user'])}](tg://user?id={id})"

                    texto_grupo = (
                                    f"💠 \| {link} *Pix automático*\n\n"
                                    f"✅ \| *R${adicionado}* Adicionado\n\n"
                                    f"💵 \| Novo Saldo *R${cliente['saldo']}*\n\n"
                                )

                    spam = arq.ler_json(ca.config)['dono']['spam']

                    for c in range(0, len(spam)):
                        th(target=func_bot.send_bot, args=(spam[c], f'{texto_grupo}', None, 'mark',)).start()
                    '''


                    '''
                    # ADICIONA % PARA A REFERENCIA
                    id_ref = cliente['referencia'] 
                    if id_ref != 'None':
                        if db.cliente(id_ref) != False:
                            porcent_refer = arq.ler_json(ca.config)['dados']['porcent_refer']
                            
                            cliente_ref = db.cliente(id_ref)
                            
                            saldo_refer = cliente_ref['saldo']
                            
                            ganho = int(porcent_refer/adicionado)

                            link =  f"[{r_texto.form(cliente_ref['user'])}](tg://user?id={id_ref})"
                            link2 =  f"[{r_texto.form(cliente_ref['user'])}](tg://user?id={id})"
                            
                            val = f"{adicionado}"
                            
                            novo_saldo_refer = saldo_refer + ganho
                            
                            cliente_ref['saldo'] = novo_saldo_refer
                            
                            th(target=func_bot.send_bot, args=(id_ref, f"💵 O Usuário {link} adicionou R${val}, você ganhou *R${r_texto.form(str(ganho))}*\n\n⥬ Novo saldo *R${r_texto.form(str(novo_saldo_refer))}*", bt, 'mark',)).start()
                            th(target=func_bot.send_log, args=(id_ref, f"📎 Ganhou R${r_texto.form(str(ganho))} \- Novo saldo R${r_texto.form(str(novo_saldo_refer))}",)).start()
                            
                            db.atualiza_cadastro(cliente_ref)
                    '''
                    
                # EXPIRA QUANDO PASSA DE 20 MINUTOS SEM PAGAR
                if time.time() > v['expiracao']:
                    arq.del_json(ca.pagamentos, 1, k)
                    
            time.sleep(0.1)


#qr_code()
