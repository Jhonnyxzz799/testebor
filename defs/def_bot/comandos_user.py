from email import message
import sys

sys.path.insert(1, '././')

from defs import func
from def_bot import func_bot
from defs import arq
from defs import ca
from defs import bin
from defs import api_pix
from defs import r_texto
from defs import db

import asyncio
import threading

pix_max = 400
pix_min = 10

comandos = [
    'start',
    'resgatar',
    'pix',
    'bin',
    'cc',
    'ccs',
    'id'
]

ok = "✅"
x= "❌"

    
def replace_comando(menssagem):
    return " ".join(menssagem.split(' ')[1:])
    
def comand_line(menssagem):
    msg_upper = menssagem.upper()
    if "CCS" in msg_upper or "CC" in msg_upper:
        return tabela_cc(menssagem)

    if "BIN" in msg_upper:
        return puxa_bin(menssagem)
    
def start(id, user, nome, menssagem):
    
    cliente = db.cliente(id)

    if cliente != False:
        
        if cliente['autorizacao'] == True:
            
            if cliente['nome'] != nome or cliente['user'] != user:
                threading.Thread(target=func_bot.send_log, args=(id, f"👁‍🗨 Nome alterado para {r_texto.form(nome)} \- {r_texto.form(user)}",)).start()
                
                cliente['nome'] = nome
                cliente['user'] = user
                
                threading.Thread(target=db.atualiza_cadastro, args=(cliente,)).start()
                
            return True
        else:
            return False
    else:
        
        temp = {}
        
        refer = replace_comando(menssagem)
        
        temp['id'] = id
        temp['user'] = user
        temp['nome'] = nome
        temp['saldo'] = 0
        temp['pontos'] = 0
        temp['compras'] = ''
        temp['gifts'] = ''
        temp['ban'] = 0
        temp['autorizacao'] = True
        temp['notificacao'] = True
        temp['referencia'] = "None"
        
        '''if refer != "":
            if refer != id:
                id_clientes = db.id_clientes()

                if refer in id_clientes:
                    cliente_ref = db.cliente(refer)
                    temp['referencia'] = refer
                    
                    bt = {
                        "inline_keyboard": [
                                                                
                        [{"text": f"Menu", "callback_data": "menu"}],

                        ]
                        }
                    
                    link =  f"[{r_texto.form(user)}](tg://user?id={id})"
                    link2 =  f"[{r_texto.form(cliente_ref['user'])}](tg://user?id={refer})"
                    
                    threading.Thread(target=func_bot.send_bot, args=(refer, f"🔹 O usuário {link} usou seu link de referência", bt, 'mark',)).start()
                    threading.Thread(target=func_bot.send_bot, args=(func_bot.id_log, f"🔹 {link} usou link de referência de {link2}", None, 'mark',)).start()
                    
                else:
                    temp['referencia'] = "None"
                
            else:
                temp['referencia'] = "None"
        else:
            temp['referencia'] = "None"'''
        
        db.cadastro(temp)
        
        threading.Thread(target=func_bot.send_log, args=(id, f"🔘 Novo usuário",)).start()
        
        return True


def pix(id, menssagem):
    
    cliente = db.cliente(id)

    if cliente != False:
        if arq.ler_json(ca.config)['dados']['pix'] == "ON":

            if menssagem.isnumeric():
                valor = menssagem
            else:
                valor = replace_comando(menssagem)
            
            if valor.isnumeric():
                valor = int(valor)
                

                
                if valor >= pix_min and valor <= pix_max:
                    texto = (
                        f"💠 ADICIONAR *R${valor}*\n\n"
                        f"💰 saldo *R${cliente['saldo']}*\n\n"
                        f"💰 Saldo após pagamento *R${cliente['saldo'] + valor}*\n\n"
                        f"_Gere o pix apenas se for pagar_\n\n"
                    )
                    
                    return {
                        "status": True,
                        "message": texto,
                        "valor": valor
                    }
                    
                else:
                        
                    return {
                        "status": False,
                        "message": f"*{x} Valor inválido*\n\nEscolha um número entre {pix_min} e {pix_max}"
                    }
                
                
            else:
                
                return {
                    "status": False,
                    "message": f"*{x} Valor inválido*\n\nEscolha um número entre {pix_min} e {pix_max}"
                }

        else:
            return {
                    "status": False,
                    "message": f"{x} Pix automático desativado"
                }
        

def tabela_cc(menssagem):
    ccs = arq.ler_json(ca.quantidade)
    precos = arq.ler_json(ca.precos)

    texto = []
    disponiveis = []
    for k,v in ccs.items():
        texto.append(f"R${precos[k]} {r_texto.form(k)} \- {v} Disponíveis")
        disponiveis.append(v)

    texto.insert(0, f"*💳 {sum(disponiveis)} CCs Disponíveis\n*")

    texto.append(f'💳 Compre em {r_texto.form(func_bot.user_store)}')
    texto.append(f'✅ Suporte {r_texto.form(func_bot.suporte)}')
    return "\n\n".join(texto).strip()


def puxa_bin(numero):
    numero = replace_comando(numero)
    print(numero)

    retorno = bin.checker(numero.strip())
    if retorno['status'] == True:
        texto = (
            f"*💳 \| BIN {numero} ENCONTRADA*\n\n"
            f"🏦  Banco {r_texto.form(retorno['banco']).title()}\n\n"
            f"📊 Level {r_texto.form(retorno['level']).title()}\n\n"
            f"🏳  Bandeira {r_texto.form(retorno['bandeira']).title()}\n\n"
            f"🌐 Tipo {r_texto.form(retorno['tipo']).title()}"
        )
        

        return texto

    else:
        return f"❌ {retorno['message'].title()}"

#print(tabela_cc())

#print(pix("1416422632", 'pix 6'))

#print(start('124', 'jhon34', '@wickjhonson', 'start 6504787'))


#print(asyncio.run(puxa_bin('650487')))