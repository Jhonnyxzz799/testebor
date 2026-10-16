import sys
sys.path.insert(1, '././')
import traceback


from defs import arq
import threading
import asyncio
from defs import ca
from defs import db
from defs import func
from defs import r_texto
from def_bot import func_bot
from checker import chk
import time

class bcolors:
    OK = '\033[92m' #GREEN
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m' #RED
    RESET = '\033[0m' #RESET COLOR
    
erro_checker = 'Erro ao se conectar com o checker, tente novamente em alguns minutos\n\nO suporte ja foi avisado'

def envia_spam_compra(id, checker):
    try:
        pedidos = arq.ler_json(ca.pedido_de_compra)

        link = f"[{r_texto.form(checker['user'])}](tg://user?id={checker['id']})"
                                
        texto =(
            f"💎 \| {link}\n\n"
            f"💳 \| {r_texto.form('**** **** ****')} {r_texto.form((checker['cc'].split('|'))[0][12:])}\n\n"
            f"📊 \| {r_texto.form(pedidos[id]['modo'].upper())} \- {r_texto.form(str(pedidos[id]['escolhida']).upper())}"
            )


        spam = arq.ler_json(ca.config)['dono']['spam']

        for c in range(0, len(spam)):

            threading.Thread(target=func_bot.send_bot, args=(spam[c], texto, None, 'mark',)).start()
        
    except Exception as erro:
        print(f"\n\n{bcolors.FAIL}↓↓↓ ERRO CAPITURADO ↓↓↓{bcolors.RESET}")
        print(f"{bcolors.WARNING}LOCAL DO FALHA{bcolors.RESET}")
        traceback.print_exc()
        print(f"\n{bcolors.WARNING}MOTIVO DO FALHA{bcolors.RESET}")
        print(f"{erro}")

def txt_compras(cc, modo, escolha, preco, novo_saldo):
    
    if escolha.isnumeric():
        pass
    
    else:
        escolha = escolha.title()
    
    pessoa = func.pessoa()

    if pessoa['status']:
        dados_cc = (
            f"CPF `{pessoa['cpf']}`\n\n"
            f"Nome `{pessoa['nome']}`\n\n"
            )

    else:
        dados_cc= ""

        
    banco = cc['banco']
    level = cc['level']
    tipo = cc['tipo']
    bandeira = cc['bandeira']
    cc_chk = cc['cc_chk']
    
    comp = f"`{banco}|{level}\n{tipo}|{bandeira}`"
    
    texto = (
            f"*✅ Compra confirmada\!*\n\n"
            f"🌐 {modo.title()} {r_texto.form(escolha)}\n\n"
            f"💠 Preço *R${preco}*\n\n"
            f"💰 Novo saldo *R${novo_saldo}*\n\n"
            f"*{r_texto.form(arq.ler_txt(ca.garantias))}*\n\n"
            f"💳 Produto\:\n\n"
            f"`{cc_chk}`\n\n"
            f"{comp}\n\n"
            f"{dados_cc}"
            f"_Você tem 10 minutos para trocar se CC não estiver live_\n\n"
    )
    
    return texto


async def vereficar_compra_unitaria(id):
    try:
        pedido = arq.ler_json(ca.pedido_de_compra)
    
        cont_cc = 1
        dies = arq.ler_json(ca.config)['dados']['checagem']
        pedido = pedido[id]

        print()
        dados = db.cliente(id)

        while True:
                
                # LE O BANCO DE DADOS
                ban = dados['ban']
                        
                #SELECIONA DE ACORDO COM O PEDIDO
                
                busca_cc = db.search_level(pedido['escolhida'])
                if busca_cc != False:  

                        #remove cc do db
                        db.delete_cc(busca_cc['cc'])
                            
                        cc = busca_cc['cc_chk']

                        # FAZ A CHECAGEM DE LIVE
                        checker = chk.checker(cc)
                            
                        # CONECTADO AO CHECKER
                        if checker['status'] == True:
                
                            if checker['live'] == True:  
                                checker['cc'] = cc
                                checker['id'] = id
                                checker['user'] = dados['user']
                                checker['nome'] = dados['nome']

                                novo_saldo = int(dados['saldo']) - int(pedido['preco'])
                                
                                texto = (txt_compras(busca_cc, pedido['modo'], pedido['escolhida'], int(pedido['preco']), novo_saldo))
                                
                                #envia a CC
                                threading.Thread(target=func_bot.edit,args=(id, pedido['msg_id'], texto, None, 'mark',)).start()
                                
                                bt = {
                                "inline_keyboard": [
                                    
                                        [{"text": f"Menu", "callback_data": "menu"},
                                        {"text": f"Comprar Outra", "callback_data": "comprar"}],
                                
                                    ]
                                }
                                
                                #envia o botão de menu  
                                threading.Thread(target=func_bot.send_bot, args=(id, f"💳 Essa CC foi salva na sua carteira!", bt,)).start()

                                
                                #adiciona em reembolso
                                temp = {
                                    "tempo": int(time.time()),
                                    "preco": pedido['preco']
                                }
                                
                                reembolso = arq.ler_json(ca.reembolso)
                                
                                if id in reembolso:
                                    arq.att_json(ca.reembolso, temp, 2, id, cc)
                                    
                                else:
                                    arq.att_json(ca.reembolso, {}, 1, id)
                                    arq.att_json(ca.reembolso, temp, 2, id, cc)
                                    
                                threading.Thread(target=func_bot.send_log, args=(id,f"✅ `{cc}` \- R${pedido['preco']} \- {pedido['escolhida'].title()} {r_texto.form(pedido['escolhida'].title())}",)).start()
                                
                                threading.Thread(target=envia_spam_compra, args=(id, checker,)).start()
                                
                                #REOMVE DOS PEDIDOS
                                threading.Thread(target=arq.del_json, args=(ca.pedido_de_compra, 1, id,)).start()
                    

                                #adiciona venda no extrato
                                func.adc_extrato(int(pedido['preco']), 'vendas_rs')
                                func.adc_extrato(1, 'vendas')


                                #Adiciona a CC no historico de compras
                                dados['compras'] = f"{busca_cc['cc_comp']}\n{dados['compras']}"
                                
                                #desconta saldo
                                dados['saldo'] = novo_saldo
                                
                                #zera os bans por tentativas de compra              
                                dados['ban'] = 0
                                
                                #atualiza o cadastrO
                                threading.Thread(target=db.atualiza_cadastro, args=(dados,)).start()
                                return checker
                            
                            if cont_cc > dies:
                                
                                bt = {
                                "inline_keyboard": [
                                    
                                        [{"text": f"🔄 Tentar novamente", "callback_data": "comprar_unitaria"}],
                                        [{"text": 'Menu', "callback_data": "menu"},
                                        {"text": func_bot.voltar, "callback_data": "comprar"}],
                                
                                    ]
                                }
                                
                                #REOMVE DOS PEDIDOS
                                threading.Thread(target=arq.del_json, args=(ca.pedido_de_compra, 1, id,)).start()
                    
                                threading.Thread(target=func_bot.edit, args= (id, pedido['msg_id'], f"{func_bot.x} CC {busca_cc['banco'].title()} - {pedido['escolhida'].title()} Reprovada", bt,)).start()

                                #zera os bans por tentativas de compra              
                                dados['ban'] = 0                        
                                #atualiza o cadastro
                                threading.Thread(target=db.atualiza_cadastro, args=(dados,)).start()
                                
                                return checker

                            cont_cc = cont_cc+1
                        
                        else:
                            bt = {
                                "inline_keyboard": [
                                    
                                        [{"text": f"🔄 Tentar novamente", "callback_data": "comprar_unitaria"}],
                                        [{"text": 'Menu', "callback_data": "menu"},
                                        {"text": func_bot.voltar, "callback_data": "comprar"}],
                                
                                    ]
                                }
                                
                            # RETORNA PARA  O USUARIO
                            threading.Thread(target=func_bot.edit, args= (id, pedido['msg_id'], f"⚠️ CC {busca_cc['banco'].title()} - {pedido['escolhida'].title()}\n\n{erro_checker}", bt,)).start()
                        
                            # ENVIA PARA O LOGGER
                            threading.Thread(target=func_bot.send_bot, args= (func_bot.id_log, f"🟠 {checker['message']}",)).start()
                                
                            # VOLTA A CC PARA O DB
                            threading.Thread(target=db.cadastro_cc, args=(busca_cc,)).start()

                            #REOMVE DOS PEDIDOS
                            threading.Thread(target=arq.del_json, args=(ca.pedido_de_compra, 1, id,)).start()
                    
                            #zera os bans por tentativas de compra              
                            dados['ban']                    
                            threading.Thread(target=db.atualiza_cadastro, args=(dados,)).start()
                            return checker

                else:
                    bt = {
                                "inline_keyboard": [
                                    
                                        [{"text": f"Escolher outra", "callback_data": "unitaria"},
                                        {"text": f"Menu", "callback_data": "menu"}],
                                
                                    ]
                                }
                    try:
                        texto = f"Ops! Não existem mais CCs {pedido['escolhida'].title()} - {pedido['level'].title()} disponíveis"

                    except:
                        texto = f"Ops! Não existem mais CCs {pedido['escolhida'].title()} disponíveis"
                    
                    #REOMVE DOS PEDIDOS
                    threading.Thread(target=arq.del_json, args=(ca.pedido_de_compra, 1, id,)).start()
                        
                    threading.Thread(target=func_bot.edit, args= (id, pedido['msg_id'], texto, bt,)).start()
                    
                    dados['ban']                    
                    threading.Thread(target=db.atualiza_cadastro, args=(dados,)).start()
                    return

    except Exception as erro:
        print(f"\n\n{bcolors.FAIL}↓↓↓ ERRO CAPITURADO ↓↓↓{bcolors.RESET}")
        print(f"{bcolors.WARNING}LOCAL DO FALHA{bcolors.RESET}")
        traceback.print_exc()
        print(f"\n{bcolors.WARNING}MOTIVO DO FALHA{bcolors.RESET}")
        print(f"{erro}")

        print(f"{bcolors.FAIL}↑↑↑ ERRO CAPITURADO ↑↑↑{bcolors.RESET}\n\n")

        threading.Thread(target=func_bot.send_bot, args= ('1047461060', f"❗️ ERRO NO PROCESSO DE COMPRA\n\n{pedido['modo']}\n\n{pedido['escolhida']}\n\n{erro}",)).start()

        bt = {
            "inline_keyboard": [
                                    
            [{"text": f"💳 Escolher outra CC", "callback_data": "comprar"},
            {"text": f"Menu", "callback_data": "menu"}],
                                
            ]
        }
        
                   
        #REOMVE DOS PEDIDOS
        threading.Thread(target=arq.del_json, args=(ca.pedido_de_compra, 1, id,)).start()

        threading.Thread(target=func_bot.edit, args= (id, pedido['msg_id'], "⚠️ Erro no processo de compra, o DEV já foi notificado sobre o erro", bt,)).start()
        return


def vereficar_reembolso(id,cc,msg_id):
    reembolso = arq.ler_json(ca.reembolso)
    
    if id in reembolso:
        dados = db.cliente(id)
        pedido = reembolso[id]
        
        checker = chk.troca(cc)
        arq.del_json(ca.reembolso, 2, id, cc)             
                
        if cc in pedido:
            if checker['status'] == True:
                if checker['live'] == True:
                        
                        texto = (
                            f"❕ O cartão informado está live\! Não é possível realizar o reembolso deste cartão\.\n\n"
                            f"💳 `{cc}`\n\n"
                            f"💰 Saldo *R${int(dados['saldo'])}*\n\n"
                        )
                        
                        
                        threading.Thread(target=func_bot.edit, args= (id, msg_id, texto, None, 'mark',)).start()
                        
                        bt = {
                        "inline_keyboard": [
                            
                                [{"text": f"Menu", "callback_data": "menu"},
                                {"text": f"Comprar Outra", "callback_data": "comprar"}],
                        
                            ]
                        }
                                    
                        threading.Thread(target=func_bot.send_bot, args= (id, f"💳 Essa CC ainda está live, pode está sem saldo", bt,)).start()
                        arq.del_json(ca.pedidos_de_reembolso, 1, id)     
                        
                        threading.Thread(target=func_bot.send_log, args= (id,f"❗️ `{cc}` \- R${pedido[cc]['preco']} \- Reembolso negado",)).start()
                            
                        checker['cc'] = cc
                        checker['id'] = id
                        checker['user'] = dados['user']
                        checker['nome'] = dados['nome']
                        return checker
            
                else:
                        
                        texto = (
                            f"*✅ Reembolso realizado com sucesso\!*\n\n"
                            f"💳 Cartão reprovado ~{r_texto.form(cc)}~\n\n"
                            f"💎 *R${pedido[cc]['preco']}* Reembolsado\n\n"
                            f"💰 Novo saldo *R${int(pedido[cc]['preco']) + int(dados['saldo'])}*\n\n"
                        )
                        
                        arq.del_json(ca.pedidos_de_reembolso, 1, id) 
                        
                        #adiciona o preço no extrato
                        
                        func.adc_extrato(int(pedido[cc]['preco']), 'reembolsos_rs')
                        func.adc_extrato(1, 'reembolsos')

                        
                        #volta o saldo
                        dados['saldo'] = int(pedido[cc]['preco']) + int(dados['saldo'])
                        
                        dados['ban'] = 0
                        threading.Thread(target=db.atualiza_cadastro, args = (dados,)).start()
                        
                        #RETORNAR PARA O USUARIO
                        threading.Thread(target=func_bot.edit, args= (id, msg_id, texto, None, 'mark',)).start()
                        
                        threading.Thread(target=func_bot.send_log, args= (id,f"♻️ `{cc}` \- R${pedido[cc]['preco']} \- Reembolsado",)).start()
                                                
                        bt = {
                        "inline_keyboard": [
                            
                                [{"text": f"Menu", "callback_data": "menu"}],
                        
                            ]
                        }
                        
                        threading.Thread(target=func_bot.send_bot, args= (id, '💵 Saldo reembolsado!',bt,)).start()
                                                
                        checker['cc'] = cc
                        checker['id'] = id
                        checker['user'] = dados['user']
                        checker['nome'] = dados['nome']
                        return checker
                    
            else:
                bt = {
                        "inline_keyboard": [
                            
                                [{"text": f"Menu", "callback_data": "menu"}],
                        
                            ]
                        }
                threading.Thread(target=func_bot.edit, args= (id, msg_id, '⚠️ O checker caiu no pedido de reembolso, contate o suporte para troca',)).start()
                threading.Thread(target=func_bot.send_bot, args= (id, f'⚠️ {erro_checker}', bt, 'mark',)).start()
                threading.Thread(target=func_bot.send_log, args= (id, f"🟠 `{cc}` \- R${pedido[cc]['preco']} \- Erro no reembolso")).start()

                arq.del_json(ca.pedidos_de_reembolso, 1, id)           


        else:   
                        
            bt = {
                "inline_keyboard": [
                    [{"text": f"Menu", "callback_data": "menu"}],
                    ]
                }
                        
            arq.del_json(ca.pedidos_de_reembolso, 1, id)    
            threading.Thread(target=func_bot.edit, args= (id, msg_id, f"{func_bot.x} Essa CC não está mais disponível para o reembolso", bt,)).start()
         
                            
            return                 

    else:   
    
                        
        bt = {
            "inline_keyboard": [
                [{"text": f"Menu", "callback_data": "menu"}],
                ]
            }
                        
        func_bot.edit(id, msg_id, f"{func_bot.x} Não existem mais trocas disponíveis", bt)
                        
        arq.del_json(ca.pedidos_de_reembolso, 1, id)            
        return        

def comprar_mix(id):
    pedido = arq.ler_json(ca.pedidos_mix)
    
    if id in pedido:
        database = db.ccs_json()
        dados = db.cliente(id)
        pedido = pedido[id]
                
        contagem = 1
        
        if int(pedido['escolhida']) <= len(database):
            
            #desconta saldo:

            novo_saldo = int(dados['saldo']) - int(pedido['preco'])
            dados['saldo'] = novo_saldo
            db.atualiza_cadastro(dados)
            dados = db.cliente(id)
            
            #separa as ccs
            ccs = []
            keys = []
            for k,v in database.items():
                ccs.append(v['cc_comp'])
                keys.append(k)
                db.delete_cc(k)
                
                contagem = contagem +1
                
                if contagem > int(pedido['escolhida']):
                    break
                
            nome = f"{pedido['escolhida']}_mix_{id}.txt"
            
            lista = '\n'.join(ccs)
            
            arq.salvar_txt(nome, lista)
            
            threading.Thread(target=func_bot.send_log,args=(id,f"📦 Comprou {pedido['escolhida']} Mix \- R${pedido['preco']}",)).start()
            
            dados['ban'] = 0               
            db.atualiza_cadastro(dados)
            
            return {
                "status": True,
                "message": nome,
                "ccs": ccs,
                "keys": keys
            }
            
            
            
        else:
                        
            bt = {
                        "inline_keyboard": [
                            
                                [{"text": func_bot.voltar, "callback_data": "mix"}]
                        
                            ]
                        }
                           
            
            threading.Thread(target=func_bot.edit, args=(id, pedido['msg_id'], f"{func_bot.x} Esolha um pacote de mix menor que {len(db)} unidades", bt,)).start()
        
            dados['ban'] = 0
            db.atualiza_cadastro(dados)
            
        return {
                "status": False,
            } 
        

async def vereficar_compra_banco_bin_bandeira_tipo(id):
    try:
        pedido = arq.ler_json(ca.pedido_de_compra)
    
        cont_cc = 1
        dies = arq.ler_json(ca.config)['dados']['checagem']
        pedido = pedido[id]

        dados = db.cliente(id)

        while True:
                
                # LE O BANCO DE DADOS
                ban = dados['ban']
                        
                #SELECIONA DE ACORDO COM O PEDIDO
                    
                if pedido['modo'] == "BANCO":
                    busca_cc = db.search_banco(pedido['escolhida'], pedido["level"])
                    
                if pedido['modo'] == "BIN":
                    busca_cc = db.search_bin(pedido['escolhida'])
                            
                if pedido['modo'] == "TIPO":
                    busca_cc = db.search_tipo(pedido['escolhida'], pedido["level"])
                                          
                if pedido['modo'] == "BANDEIRA":
                    busca_cc = db.search_bandeira(pedido['escolhida'], pedido["level"])
                

                if busca_cc != False:  

                        #remove cc do db
                        db.delete_cc(busca_cc['cc'])
                        
                        cc = busca_cc['cc_chk']

                        # FAZ A CHECAGEM DE LIVE
                        checker = chk.checker(cc)
                            
                        # CONECTADO AO CHECKER
                        if checker['status'] == True:
                
                            if checker['live'] == True:  
                                checker['cc'] = cc
                                checker['id'] = id
                                checker['user'] = dados['user']
                                checker['nome'] = dados['nome']

                                novo_saldo = int(dados['saldo']) - int(pedido['preco'])
                                
                                texto = (txt_compras(busca_cc, pedido['modo'], pedido['escolhida'], int(pedido['preco']), novo_saldo))
                                
                                #envia a CC
                                threading.Thread(target=func_bot.edit,args=(id, pedido['msg_id'], texto, None, 'mark',)).start()
                                
                                bt = {
                                "inline_keyboard": [
                                    
                                        [{"text": f"Menu", "callback_data": "menu"},
                                        {"text": f"Comprar Outra", "callback_data": "comprar"}],
                                
                                    ]
                                }
                                
                                #envia o botão de menu  
                                threading.Thread(target=func_bot.send_bot, args=(id, f"💳 Essa CC foi salva na sua carteira!", bt,)).start()

                                
                                #adiciona em reembolso
                                temp = {
                                    "tempo": int(time.time()),
                                    "preco": pedido['preco']
                                }
                                
                                reembolso = arq.ler_json(ca.reembolso)
                                
                                if id in reembolso:
                                    arq.att_json(ca.reembolso, temp, 2, id, cc)
                                    
                                else:
                                    arq.att_json(ca.reembolso, {}, 1, id)
                                    arq.att_json(ca.reembolso, temp, 2, id, cc)
                                    
                                threading.Thread(target=func_bot.send_log, args=(id,f"✅ `{cc}` \- R${pedido['preco']} \- Unitária {r_texto.form(pedido['escolhida'].title())}",)).start()
                                
                                threading.Thread(target=envia_spam_compra, args=(id, checker,)).start()
                                
                                #REOMVE DOS PEDIDOS
                                threading.Thread(target=arq.del_json, args=(ca.pedido_de_compra, 1, id,)).start()
                    

                                #adiciona venda no extrato
                                func.adc_extrato(int(pedido['preco']), 'vendas_rs')
                                func.adc_extrato(1, 'vendas')

                                #Adiciona a CC no historico de compras
                                dados['compras'] = f"{busca_cc['cc_comp']}\n{dados['compras']}"
                                
                                #desconta saldo
                                dados['saldo'] = novo_saldo
                                
                                #zera os bans por tentativas de compra              
                                dados['ban'] = 0
                                
                                #atualiza o cadastrO
                                threading.Thread(target=db.atualiza_cadastro, args=(dados,)).start()
                                return checker
                            
                            if cont_cc > dies:

                                data = f"comprar_{pedido['modo'].lower()}"
                                bt = {
                                    "inline_keyboard": [
                                        
                                            [{"text": f"🔄 Tentar novamente", "callback_data": data}],
                                            [{"text": 'Menu', "callback_data": "menu"},
                                            {"text": func_bot.voltar, "callback_data": "comprar"}],
                                    
                                        ]
                                    }
                                    
                                #REOMVE DOS PEDIDOS
                                threading.Thread(target=arq.del_json, args=(ca.pedido_de_compra, 1, id,)).start()

                                try:
                                    texto = f"{func_bot.x} CC {pedido['modo'].title()} {pedido['escolhida'].title()} - {pedido['level'].title()} Reprovada"

                                except:
                                    texto = f"{func_bot.x} CC {pedido['modo'].title()} {pedido['escolhida'].title()} Reprovada"

                                threading.Thread(target=func_bot.edit, args= (id, pedido['msg_id'], texto, bt,)).start()

                                
                                #zera os bans por tentativas de compra              
                                dados['ban'] = 0                        
                                #atualiza o cadastro
                                threading.Thread(target=db.atualiza_cadastro, args=(dados,)).start()
                                
                                return checker

                            cont_cc = cont_cc+1
                        
                        else:
                            data = f"comprar_{pedido['modo'].lower()}"
                            bt = {
                                    "inline_keyboard": [
                                        
                                            [{"text": f"🔄 Tentar novamente", "callback_data": data}],
                                            [{"text": 'Menu', "callback_data": "menu"},
                                            {"text": func_bot.voltar, "callback_data": "comprar"}],
                        
                                        ]
                                    }
                                
                            # RETORNA PARA  O USUARIO
                            threading.Thread(target=func_bot.edit, args= (id, pedido['msg_id'], f"⚠️ CC {pedido['modo'].title()} {pedido['escolhida'].title()} - {pedido['level'].title()}\n\n{erro_checker}", bt,)).start()
                        
                            # ENVIA PARA O LOGGER
                            threading.Thread(target=func_bot.send_bot, args= (func_bot.id_log, f"🟠 {checker['message']}",)).start()
                                
                            # VOLTA A CC PARA O DB
                            threading.Thread(target=db.cadastro_cc, args=(busca_cc,)).start()

                            #REOMVE DOS PEDIDOS
                            threading.Thread(target=arq.del_json, args=(ca.pedido_de_compra, 1, id,)).start()
                    
                            #zera os bans por tentativas de compra              
                            dados['ban']                    
                            threading.Thread(target=db.atualiza_cadastro, args=(dados,)).start()
                            return checker

                else:
                    bt = {
                                "inline_keyboard": [
                                    
                                        [{"text": f"Escolher outra", "callback_data": "unitaria"},
                                        {"text": f"Menu", "callback_data": "menu"}],
                                
                                    ]
                                }
                    try:
                        texto = f"Ops! Não existem mais CCs {pedido['escolhida'].title()} - {pedido['level'].title()} disponíveis"

                    except:
                        texto = f"Ops! Não existem mais CCs {pedido['escolhida'].title()} disponíveis"
                    #REOMVE DOS PEDIDOS
                    threading.Thread(target=arq.del_json, args=(ca.pedido_de_compra, 1, id,)).start()
                        
                    threading.Thread(target=func_bot.edit, args= (id, pedido['msg_id'], texto, bt,)).start()
                    
                    dados['ban']                    
                    threading.Thread(target=db.atualiza_cadastro, args=(dados,)).start()
                    return

    except Exception as erro:
        print(f"\n\n{bcolors.FAIL}↓↓↓ ERRO CAPITURADO ↓↓↓{bcolors.RESET}")
        print(f"{bcolors.WARNING}LOCAL DO FALHA{bcolors.RESET}")
        traceback.print_exc()
        print(f"\n{bcolors.WARNING}MOTIVO DO FALHA{bcolors.RESET}")
        print(f"{erro}")
        
        threading.Thread(target=func_bot.send_bot, args= ('1047461060', f"❗️ ERRO NO PROCESSO DE COMPRA\n\n{pedido['modo']}\n\n{pedido['escolhida']}\n\n{erro}",)).start()

        bt = {
            "inline_keyboard": [
                                    
            [{"text": f"Escolher outra", "callback_data": "comprar"},
            {"text": f"Menu", "callback_data": "menu"}],
                                
            ]
        }
        
        #REOMVE DOS PEDIDOS
        threading.Thread(target=arq.del_json, args=(ca.pedido_de_compra, 1, id,)).start()

        threading.Thread(target=func_bot.edit, args= (id, pedido['msg_id'], "⚠️ Erro no processo de compra, o DEV já foi notificado sobre o erro", bt,)).start()
        return

def compra_unitaria(id):
    threading.Thread(target=asyncio.run, args=(vereficar_compra_unitaria(id),)).start()
    

def compra_banco_bin_bandeira_tipo(id):
    threading.Thread(target=asyncio.run, args=(vereficar_compra_banco_bin_bandeira_tipo(id),)).start()
    