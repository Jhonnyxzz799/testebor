import sys

sys.path.insert(1, 'defs')
#sys.path.insert(1, './')

import threading
import time
import os.path
import os
import json
import zipfile
from datetime import datetime

from defs import r_texto
from defs.checker import chk
import random

from aiogram.types import InputTextMessageContent, InlineQueryResultArticle
from defs import separador
from defs import arq
from defs import bin
from def_bot import func_bot
from defs import ca
from defs import db
import api_pix
from datetime import date

import requests
from datetime import datetime


def hora_hora():
    return f"{datetime.now():%d-%m-%Y-%H-%M-%S}"

def dados():
    return arq.ler_json(ca.config)['dados']

def dono():
    return arq.ler_json(ca.config)['dono']

def checker():
    return arq.ler_json(ca.config)['cheker']
    


def att_quantidade_ccs():
    if True:
        try:
            time.sleep(1)
            database = db.ccs_json()
            precos = arq.ler_json(ca.precos)
            quantidade = arq.ler_json(ca.quantidade)
            
            disponiveis = {}

            for k,v in database.items():
                if v['level'] in precos:
                    if v['level'] not in disponiveis:
                        disponiveis[v['level']] = 1
                        
                    else:
                        disponiveis[v['level']] = disponiveis[v['level']] +1
                    
                
            return disponiveis 
        except:
            pass
 
 
def atualizar_quantidade_ccs():
    while True:
        qtd_atiga = arq.ler_json(ca.quantidade)
        qtd_nova = att_quantidade_ccs()
        
        try:
            if qtd_atiga != qtd_nova:
                arq.salvar_json(ca.quantidade, qtd_nova)
                #print('QUANTIDADE ATUALIZADA')
                
        except:
            pass

def compra_disponivel(id):
    
    cliente = db.cliente(id)

    pedido_de_compra = arq.ler_json(ca.pedido_de_compra)
    
    pedidos_mix = arq.ler_json(ca.pedidos_mix)

    pedido_de_reembolso = arq.ler_json(ca.pedidos_de_reembolso)

    
    api = {
        "status": False,
        "message": '',
        
    }
        
    if vendas_on():
        api['status']=True
        if cliente != False:

            if cliente['autorizacao']:
                api['status']=True
                
                if id not in pedido_de_compra and id not in pedidos_mix and id not in pedido_de_reembolso:
                    api['status']=True
                
                else:
                    api['status']=False
                    api['message']= '⚠️ Aguarde seu último pedido de compra ser finalizado, caso tente mais vezes você será banido da store'
                    cliente['ban'] = cliente['ban'] +1
                    
                    db.atualiza_cadastro(cliente)
                                    
                    func_bot.send_log(id,'⚠️ Tentativa de 2 compras ao mesmo tempo aguarde e nao tente mais para evitar ban da store')
                    
                    verefica_ban(id)
                    
            else:
                api['status']=False
                api['message']= f'❌ Você foi banido'
        
    else:
        api['status']=False
        api['message']= '⚠️ As vendas estão OFF por enquanto estamos em manutencao aguarde'
    
    return api

def pessoa():

    headers = {
            'authority': 'www.4devs.com.br',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
            'sec-ch-ua-platform': '"Windows"',
            'content-type': 'application/x-www-form-urlencoded',
            'accept': '*/*',
            'origin': 'https://www.4devs.com.br',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.4devs.com.br/gerador_de_pessoas',
            'accept-language': 'pt-BR,pt;q=0.9',
        }

    data = {
            'acao': 'gerar_pessoa',
            'sexo': 'I',
            'pontuacao': 'S',
            'idade': '0',
            'cep_estado': '',
            'txt_qtde': '1',
            'cep_cidade': ''
            }

    try:
            response = requests.post('https://www.4devs.com.br/ferramentas_online.php', headers=headers, data=data)
                
            r = (response.json())

            api = {
                "status": True,
                "cpf": r['cpf'],
                "nome": r['nome'],
            }
            
            return api
    except :
        api = {
                "status": False
            }

        return api



def vendas_on():
    
    vendas = arq.ler_json(ca.config)['dados']['vendas_cc']
    
    if vendas == 'ON':
        return True

    else:
        return False

def verefica_ban(id):
    
    cliente = db.cliente(id)
    maximo = 3
    
    
    if cliente != False:
        if cliente['ban'] > maximo and cliente['autorizacao'] == True:
                    
            cliente['autorizacao'] = False
            func_bot.send_bot(id, f"{func_bot.x} Você foi banido")
                    
            db.atualiza_cadastro(cliente)
            
            func_bot.send_log(id, '🔒 Usuário banido pelo bot')

            return {
                "status": True,
                "message": "Voce foi banido"
            }
         
        else:   
            return False

    else:
        return {
                "status": True,
                "message": "Usuário não encontrado"
            }

def dia_extrato():
    
    data = date.today().strftime('%d/%m/%Y')
    
    extrato = arq.ler_json(ca.extrato)

    temp = {
        "entrada_pix_rs": 0,
        "entrada_gift_rs": 0,
        "vendas_rs": 0,
        "vendas": 0,
        "reembolsos_rs": 0,
        "reembolsos": 0
    }

    if data not in extrato:
        arq.att_json(ca.extrato, temp, 1, data)
        
def hoje():
    return date.today().strftime('%d/%m/%Y')

def adc_extrato(valor, key):
    dia_extrato()
    
    data = date.today().strftime('%d/%m/%Y')
    
    extrato = arq.ler_json(ca.extrato)
    novo_valor = extrato[data][key] + valor
    arq.att_json(ca.extrato, novo_valor, 2, data, key)
    
    return valor

def adiciona_material():
    while True:
        time.sleep(6)
        linhas = arq.ler_txt(ca.temp_cc).splitlines()
        arq.limpar_txt(ca.temp_cc)

        qtd = len(linhas)
        
        adicionadas = 0
        repetidas = 0
        nao_adicionadas = 0
        em_branco = 0
        esteve_em_estoque = 0
        temp = {}
        if qtd > 0:
            novas = {}
            
            estocadas = arq.ler_json(ca.adicionadas)['adicionadas']

            for c in range(0, qtd):
                if len(linhas[c]) >= 24:
                    cc_separada = separador.separar_cc(linhas[c])
                    
                    try:
                            
                        if cc_separada != None:
                            print(f"\r{c+1}/{qtd} | {cc_separada}", end="", flush=True)
                            bin_cc = bin.checker(cc_separada[:6])
                            if bin_cc['status'] == True:
                                cc_montada = f"{cc_separada}|{bin_cc['bandeira']}|{bin_cc['tipo']}|{bin_cc['level']}|{bin_cc['banco']}|{bin_cc['pais']}"
                        
                            else:
                                cc_montada = f"{cc_separada}|INDEFINIDO|INDEFINIDO|INDEFINIDO|INDEFINIDO|INDEFINIDO"
                                
                            cc_montada = cc_montada.split("|")
                            
                            if len(cc_montada) == 9:
                                cc = cc_montada[0]
                                mes = cc_montada[1]
                                ano = cc_montada[2]
                                cvv = cc_montada[3]
                                bandeira = cc_montada[4]
                                tipo = cc_montada[5]
                                level = cc_montada[6]
                                banco = cc_montada[7]
                                pais = cc_montada[8].replace('\n','').strip()
                                    
                                if cc not in estocadas:
                                    
                                    if db.cc_numero(cc) == False:
                                        
                                        novas[cc] = {
                                            "cc": cc,
                                            "mes": mes,
                                            "ano": ano,
                                            "cvv": cvv,
                                            "bandeira": bandeira,
                                            "tipo": tipo,
                                            "level": level,
                                            "banco": banco,
                                            "pais": pais,
                                            "cc_chk": f"{cc}|{mes}|{ano}|{cvv}",
                                            "cc_comp": f"{cc}|{mes}|{ano}|{cvv}|{bandeira}|{tipo}|{level}|{banco}|{pais}"
                                        }
                                        db.cadastro_cc(novas[cc])
                                        
                                        #arq.att_json(ca.db_cc, temp[cc], 1, cc)
                                        
                                        #send_bot(id_dono, f"✅  [{c+1}/{qtd}]  {cc}  {level}")
                                        
                                        adicionadas = adicionadas + 1

                                        estocadas.append(cc)
                                        
                                    else:
                                        #send_bot(id_dono, f"🔄  [{c+1}/{qtd}]  {cc}  {level}")

                                        repetidas = repetidas + 1
                            
                                else:
                                    esteve_em_estoque = esteve_em_estoque +1
                            else:
                                #send_bot(id_dono, f"❌  [{c+1}/{qtd}]  {cc_separada}")
                                nao_adicionadas = nao_adicionadas + 1
                                pass 
                                        
                        else:
                            #send_bot(id_dono, f"❌  [{c+1}/{qtd}]  {linhas[c]}")
                            nao_adicionadas = nao_adicionadas + 1
                            pass
                        
                    except:
                        pass
                
                else:
                        #send_bot(id_dono, f"❌  [{c+1}/{qtd}]  {linhas[c]}")
                        em_branco = em_branco + 1
            
            print(f"\nMATERIAL ADICIONADO\n")
            bt = {
                        "inline_keyboard": [
                        [{"text": f"Menu", "callback_data": "menu"}],
                        ]
                }    
            
            arq.att_json(ca.adicionadas, estocadas, 1, 'adicionadas')

            func_bot.send_bot(func_bot.id_dono, (
                f"💳 CC's lidas {adicionadas + nao_adicionadas + repetidas + esteve_em_estoque}\n\n"
                f"📃 {em_branco} Linhas em branco\n\n"
                f"✅ {adicionadas} Novas CCs\n\n"
                f"❌ {nao_adicionadas} Inválidas\n\n"
                f"🔄 {repetidas} Repetidas\n\n"
                f"♻️ {esteve_em_estoque} Estiveram no estoque\n\n"
                
                ),bt )
        
            time.sleep(1)
        else:
            time.sleep(1)



def carteira(id):
    
    cliente = db.cliente(id)
    
    if cliente != False:
        lista = cliente['compras'].splitlines()

        ultimas = []
        
        
        for c in range(0, 5):
            try:
                ultimas.append(f"\n\n`{lista[c]}`")
            except:
                pass
        compras = "".join(ultimas)
        
        link = r_texto.form(f"{func_bot.url_store}?start={id}")
        
        
        text = (
            f"[*💰 SUA CARTEIRA PESSOAL*](https://telegra.ph/file/178a32137c85b61d153fe.png)\n\n\n"
            
            f"➤ ID\: `{id}`\n\n"
            f"✪ Saldo:\: *R${cliente['saldo']}*\n\n"
            f"➤ GIFTs\: *{len(cliente['gifts'].strip().splitlines())}*\n\n"
             f"➤ Compras\: *{len(cliente['compras'].strip().splitlines())}*\n\n"
            
    
        )
        return text.strip()
    
    else:
        return 'Usuário não encontrado'

def ranking():
    import operator

    while True:
        clientes = db.clientes_json()
        #print(clientes)

        ranking = {}
        saldo = {}

        for k,v in clientes.items():
            compras = len(v['compras'].strip().splitlines())

            if compras > 0 and v['user'] != None and v['user'] != "@None" and k != func_bot.id_dono:
                ranking[k] = compras

            if v['saldo'] > 0 and v['user'] != None and v['user'] != "@None" and k != func_bot.id_dono:
                saldo[k] = v['saldo']



        sortedDict = sorted(ranking.items(), key=operator.itemgetter(1), reverse=True)
        sortedDictsaldo = sorted(saldo.items(), key=operator.itemgetter(1), reverse=True)

        texto = ["*🏆 RANKING*\n\n*MAIS COMPRAS*\n"]

        premio = ['🥇','🥈','🥉']
        
        for c in range(0,3):
            try:
                id = sortedDict[c][0]
                compras = sortedDict[c][1]
                texto.append(f"{premio[c]} {compras} COMPRAS \- {r_texto.form(clientes[id]['user'])}\n")
            except:
                pass

        texto.append("\n*MAIS SALDO*\n")

        for c in range(0,3):
            try:
                id = sortedDictsaldo[c][0]
                saldo = sortedDictsaldo[c][1]
                texto.append(f"{premio[c]} R${saldo} SALDO \- {r_texto.form(clientes[id]['user'])}\n")
            except:
                pass

        texto = "\n".join(texto)

        arq.salvar_txt(ca.ranking_texto, texto)
        time.sleep(5)


def rate():
    registro = arq.ler_linhas(ca.logger_cc)
    
    aprovadas = 0
    reprovadas = 0

    for c in range(0,len(registro)):

        if "✅" in registro[c]:
            aprovadas = aprovadas + 1
      
        if "❌" in registro[c]:
            reprovadas = reprovadas + 1

    
    total = aprovadas + reprovadas

    try:
        rate = (aprovadas/total)*100
        rate = f"{rate:.0f}%"

    except: 
        rate = "Rate não disponível"

    return rate

