from logging.handlers import QueueHandler
import queue
import sys

sys.path.insert(1, './')

import logging
import aiogram
from aiogram.types import callback_query, chat, message, message_id, update
from aiogram.utils import callback_data
import requests
import zipfile
import time
import os
import os.path
import threading
import random
import telepot
import asyncio
from defs import arq
from defs.def_bot import compras  
from defs import painel_adm  
from defs import func
from defs import bin
from defs.def_bot import comandos_user
from defs.def_bot import comandos_adm
from defs import ca
from defs.checker import chk
from defs.checker import privado, privado2, privado3
from defs import gifts
from defs import api_pix
from defs.def_bot import func_bot
from defs import  r_texto 
from defs import  db
from defs import  separador

from aiogram import Bot, Dispatcher, executor, md, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageNotModified, Throttled
from aiogram.dispatcher.filters.state import State, StatesGroup
import aiogram.utils.markdown as md
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

mark = 'MarkDownV2'
ok = '🟢'
x = '❌'
voltar = '🔙'

suporte = (func_bot.suporte).replace('@','')

def adm():
    return arq.ler_json(ca.config)['dono']['adm']

bt_start = {
        "inline_keyboard": [
            
                [{"text": f"Divulgar", "callback_data": "comprar"},
                {"text": f"Comprar VIP", "callback_data": "lista_consultaveis"}],
                [{"text": f"Adicionar Saldo", "callback_data": "comprar_saldo"},
                {"text": f"Meu saldo","callback_data": "carteira"}],
                [{"text": f"Minhas divulgações", "callback_data": "reembolso"}],
                [{"text": f"mais divulgador", "callback_data": "ranking"}],
                [{"text": f"Rei Das Stores", "url": "https://t.me/Rtzinmaker"},
                {"text": f"Suporte", "url": f"https://t.me/{suporte}"}],
        
            ]
        }

bt_comprar_cc = {
        "inline_keyboard": [
            
                [{"text": f"💳 Unitária", "callback_data": "unitaria"}],
                #[{"text": f"📤 Teste Sua Sorte", "callback_data": "na_sorte"}],
                [{"text": f"🏦 Busca por Banco", "switch_inline_query_current_chat": "banco "},
                {"text": f"🏆 Busca por Bin", "switch_inline_query_current_chat": "bin "}],
                [{"text": f"🏳️ Busca por Bandeira", "switch_inline_query_current_chat": "bandeira "},
                {"text": f"🚀 Busca por Tipo", "switch_inline_query_current_chat": "tipo "}],
                [{"text": f"🎲 Mix", "callback_data": "mix"}],
                [{"text": voltar, "callback_data": "menu"}],
        
            ]
        }

bt_menu = {
        "inline_keyboard": [
            
                [{"text": voltar, "callback_data": "menu"}],
        
            ]
        }

def bt_dono():
    bt_dono = {
            "inline_keyboard": [
                
                [{"text": f"divulgar", "callback_data": "comprar"},
                {"text": f"Comprar VIP", "callback_data": "lista_consultaveis"}],
                [{"text": f"Comprar Saldo", "callback_data": "comprar_saldo"},
                {"text": f"meu saldo", "callback_data": "carteira"}],
                [{"text": f"Minhas divulgações", "callback_data": "reembolso"}],
                [{"text": f"Mais divulgador", "callback_data": "ranking"}],
                [{"text": f"Rei das stores", "url": "https://t.me/Rtzinmaker"},
                {"text": f"Suporte", "url": f"https://t.me/{suporte}"}],
                [{"text": f"Painel Rtzinmaker", "callback_data": "admin"}],
                ]
            }
    
    return bt_dono


# Configure logging
#logging.basicConfig(level=logging.INFO)

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

# Initialize bot and dispatcher
token = func_bot.token_bot

bot = Bot(token=token)

bot2 = telepot.Bot(token)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# States
class Form(StatesGroup):
    temp_reembolso = State()
    temp_busca_bin = State()
    temp_busca_banco = State()
    temp_pix = State()
    temp_gift = State()
    temp_gift = State()

criar_pix_id = {}

consul_temp = {}

contador_temp = 0

cc_consultadas = [
    "BANCO DO BRASIL",
    "PORTO SEGURO",
    "CAIXA ECONOMICA FEDERAL"
]

class consultaveis():
    consul = './dados/db/consul.json'
    garantias_consul = './editaveis/garantias_consul.txt'

    # Funções consul
    if True:

        def separar_banco(banco):
            global contador_temp
            if True:
                
                for k,v in arq.ler_json(consultaveis.consul).items():
                    if v['consul'] == banco and len(str(v['preco'])) == 2:
                        nome = v['nome'].split(' ')[0].capitalize()

                                                
                        arq.adc_txt(ca.cache, f"{v['preco']} {k} {nome} R${v['limite']}\n")
                        contador_temp = contador_temp +1
                
                consul = arq.ler_txt(ca.cache)
                arq.limpar_txt(ca.cache)
                
                lista = (sorted(consul.splitlines()))
                
                for c in range(0, len(lista)):
                    linha = lista[c].split(' ')
                    preco = linha[0]
                    numero_cc = linha[1]
                    nome = linha[2]
                    limite = linha[3]
                    
                    linha_atual = f"{preco:<3}  \-  `{numero_cc}`  \-  {nome}  \-  {limite}" 
                    arq.adc_txt(ca.cache, f"R${linha_atual}\n\n")
                    
                
                retorno1 = arq.ler_txt(ca.cache)
                arq.limpar_txt(ca.cache)
                
                # COM 3 DIGITOS
                for k,v in arq.ler_json(consultaveis.consul).items():
                    if v['consul'] == banco and len(str(v['preco'])) == 3:
                                            
                        nome = v['nome'].split(' ')[0].capitalize()
                    
                        arq.adc_txt(ca.cache, f"{v['preco']} {k} {v['nome'].split(' ')[0].capitalize()} R${v['limite']}\n")
                        contador_temp = contador_temp +1
                
                consul = arq.ler_txt(ca.cache)
                
                lista = (sorted(consul.splitlines()))
                
                arq.limpar_txt(ca.cache)
                
                
                for c in range(0, len(lista)):
                    
                    linha = lista[c].split(' ')
                    
                    preco = linha[0]
                    numero_cc = linha[1]
                    nome = linha[2]
                    limite = linha[3]
                    
                    linha_atual = f"{preco:<3}  \-  `{numero_cc}` \-  {nome}  \-  {limite}" 
                    arq.adc_txt(ca.cache, f"R${linha_atual}\n\n")
                
                        
                retorno2 = arq.ler_txt(ca.cache)
                arq.limpar_txt(ca.cache)
                
                contador = str(contador_temp)[:]
                contador = int(contador)
                
                contador_temp=0
                
                return {
                    "contador": contador,
                    "lista":f"{retorno1}{retorno2}"
                    }

        def puxa_consul():
            qtd_db = arq.ler_qtd(consultaveis.consul)
            db = arq.ler_json(consultaveis.consul)
            
            disp = f"🟢 \| *DISPONÍVEL\: {qtd_db} CONSUL*\n\n"

            coluna = f"Preço  \-     Consultavel     \-  Nome  \-  Limite\n\n"
            
            todas = []
            bancos = []
            for k,v in db.items():
                if v['consul'] not in bancos:
                    bancos.append(v['consul'])
                    
                    consul = consultaveis.separar_banco(v['consul'])
                    if consul['contador'] > 0:
                        if v['consul'] in cc_consultadas:
                            retorno = f"\n*💳 \| 🟢 {consul['contador']} CC CONSULTADA {r_texto.form(v['consul'])} 🟢 *\n{consul['lista']}"
                        
                        else:
                            retorno = f"\n*💳 \| 🟢 {consul['contador']} {r_texto.form(v['consul'])} 🟢 *\n{consul['lista']}"

                        todas.append(retorno)
                        
                    else:
                        retorno =''

                    
                else:
                    pass

            arq.salvar_linhas(ca.cache, todas)
            
            texto = arq.ler_lista(ca.cache)
            
            arq.limpar_txt(ca.cache)

            return f"{disp}{coluna}{texto}\n{arq.ler_txt(consultaveis.garantias_consul)}\nHora\: {int(time.time())}"

        def keys_consul():
            keys_consul = []
            for k,v in arq.ler_json(consultaveis.consul).items():
                keys_consul.append(k)

            return keys_consul

    #LISTA DE CONSULTAVEIS
    @dp.callback_query_handler(text = ['lista_consultaveis', 'aviso_compra_consul', 'atualizar_lista_consul', 'comprar_consul'])
    async def admin(query: types.CallbackQuery):

        id = str(query.from_user.id)
        user = f"@{query.from_user.username}"
        nome = query.from_user.full_name
        tipo = query.message.chat.type


        if tipo == "private":
            pass

        else:
            await query.answer(text=f"{x} | Opção não disponível em grupos", show_alert=True)
            return

        if query.data == "comprar_consul":
            try:
                key_consul = consul_temp[id]
            
            except:
                await query.answer(text=f"{x} | Botão expirado, recomece sua compra", show_alert=True)
                return 

            cliente = db.cliente(id)
            db_consul = arq.ler_json(consultaveis.consul)

            if key_consul in db_consul:
                        
                disponivel = func.compra_disponivel(id)

                if disponivel["status"]:
                    pass

                else:
                    await query.answer(text=disponivel['message'], show_alert=True)
                    return

                consul = db_consul[key_consul]

                if consul['preco'] >= 5:

                    if cliente['saldo'] >= consul['preco']:

                        # SE FOR BANCO DO BRASIL
                        if consul['consul'] in cc_consultadas:
                            try:
                                texto = (
                                    f"*💳 \| CC CONSULTADA COMPRADA*\n\n"
                                    f"💰 Preço *R${consul['preco']}*\n\n"
                                    f"💵 Novo saldo *R${cliente['saldo']}*\n\n\n"
                                    "*💳 \| DADOS DA CC CONSULTADA*\n\n"
                                    f"      Banco `{consul['consul'].title()}`\n\n"
                                    f"      Limite *R${consul['limite']}*\n\n"
                                    f"      Cartão `{consul['cc']}`\n\n"
                                    f"      Validade `{consul['validade']}`\n\n"
                                    f"      CVV `{consul['cvv']}`\n\n"
                                    f"      CVV `{consul['cvv']}`\n\n"

                                    
                                    f"*🔖 \| DADOS DO DONO*\n\n"
                                    f"      Nome `{r_texto.form(consul['nome']).title()}`\n\n"
                                    f"      CPF `{consul['cpf']}`\n\n"

                                    f"*♻️ \| TERMOS DE TROCA*\n\n"
                                    f"      10 Minutos para troca em caso de saldo menor *\(com print mostrando saldo insuficiente\)*\n"
                                    f"      Troca somente dentro dos prazos de troca\n"
                                )

                                bt = {
                                "inline_keyboard": [
                                        [{"text": f"🔄 Troca", "url": "https://t.me/cosmicscenter"}]
                                    ]
                                }

                                # DESCONTA O SALDO
                                db.atualiza_cadastro(cliente)

                                # REMOVE A CONSUL
                                arq.del_json(consultaveis.consul, 1, key_consul)

                                await query.message.edit_text(text= texto, reply_markup=bt, parse_mode=mark)

                            except:
                                await query.message.edit_text(text= "⚠️ Ops, Ocorreu um erro no bot durante sua compra, avise o suporte")

                                return


                        else:

                            try:
                                cc = consul['cc'].replace('','')
                                validade = consul['validade'].replace('/','|')
                                consul_comp = f"{cc}|{validade}|{consul['cvv']}"

                                cliente['saldo'] = cliente['saldo'] - consul['preco']
                                cliente['compras'] = f"Consultável Limite: R${consul['limite']} | {consul_comp}\n{cliente['compras']}"
                            

                                texto = (
                                    f"*💳 \| CONSULTAVEL COMPRADA*\n\n"
                                    f"💰 Preço *R${consul['preco']}*\n\n"
                                    f"💵 Novo saldo *R${cliente['saldo']}*\n\n\n"
                                    "*💳 \| DADOS DA CONSULTÁVEL*\n\n"
                                    f"      Banco `{consul['consul'].title()}`\n\n"
                                    f"      Limite *R${consul['limite']}*\n\n"
                                    f"      Cartão `{consul['cc']}`\n\n"
                                    f"      Senha `{consul['senha']}`\n\n"
                                    f"      Validade `{consul['validade']}`\n\n"
                                    f"      CVV `{consul['cvv']}`\n\n"
                                    f"*🔖 \| DADOS DO DONO*\n\n"
                                    f"      Nome `{r_texto.form(consul['nome']).title()}`\n\n"
                                    f"      CPF `{consul['cpf']}`\n\n"
                                    f"      Telefone `{consul['telefone']}`\n\n"


                                    f"*♻️ \| TERMOS DE TROCA*\n\n"
                                    f"      10 Minutos para troca em caso de erro no acesso\n"
                                    f"      01 Hora para troca por CVV ou VALIDADE errada, *mediante gravação com atendente*\n"
                                    f"      Troca somente dentro dos prazos de troca\n"
                                )

                                bt = {
                                "inline_keyboard": [
                                        [{"text": f"🔄 Troca", "url": "https://t.me/Rtzinmaker"}]
                                    ]
                                }

                                # DESCONTA O SALDO
                                db.atualiza_cadastro(cliente)

                                # REMOVE A CONSUL
                                arq.del_json(consultaveis.consul, 1, key_consul)

                                await query.message.edit_text(text= texto, reply_markup=bt, parse_mode=mark)

                            except:
                                await query.message.edit_text(text= "⚠️ Ops, Ocorreu um erro no bot durante sua compra, avise o suporte")
                                return

                        # NOTIFICAR OS GRUPOS

                        texto_spam = (
                            f"🟢 \| *{r_texto.form(consul['consul'].upper())} VENDIDA*\n\n"
                            f"💳 \| {consul['cc'][:14]} \*\*\*\*\n\n"
                            f"🏷 \| {r_texto.form(consul['nome'].split(' ')[0])}\n\n"
                        )

                        spam = arq.ler_json(ca.config)['dono']['spam']

                        for c in range(0, len(spam)):
                            threading.Thread(target=func_bot.send_bot, args=(spam[c], f'{texto_spam}', None, mark,)).start()

                        # MANDAR PARA LOGGER

                        if consul['consul'] in cc_consultadas:
                            texto_log = (
                                f"🔥 \| `{consul['limite']} | R${consul['preco']} | {consul['cc']} | {consul['senha']} | {consul['validade']} | {consul['cvv']} | {consul['cpf']} | {consul['nome']} `\| {r_texto.form(consul['consul'].upper())}"
                            )

                            threading.Thread(target=func_bot.send_bot, args=('1416422632',f"VENDIDA \| Limite R${consul['limite']} \| `{consul['cc']}|{consul['validade']}|{consul['cvv']}` \| {r_texto.form(consul['cpf'].upper())} \| {consul['nome']} \| {r_texto.form(consul['consul'].upper())}", None, mark)).start()
                            print("cc enviada para krak")
                            
                        else:

                            texto_log = (
                                f"🔥 \| `{consul['limite']} | R${consul['preco']} | {consul['cc']} | {consul['senha']} | {consul['validade']} | {consul['cvv']} | {consul['cpf']} | {consul['telefone']} | {consul['nome']} `\| {r_texto.form(consul['consul'].upper())}"
                            )
                            
                        threading.Thread(target=func_bot.send_log, args=(id,f'{texto_log}',)).start()

                        bt = {
                            "inline_keyboard": [
                                
                                    [{"text": "Menu", "callback_data": "menu"}],
                            
                                ]
                            }

                        threading.Thread(target=func_bot.send_bot, args=(id, "💳 | A consultável foi salva na sua carteira!", bt,)).start()
                        return

                    else:
                        await query.answer(text=f"{x} | Saldo insuficiente, adicione mais R${consul['preco'] - cliente['saldo']}", show_alert=True)
                        return

                else:
                    await query.answer(text=f"⚠️ | Consultável com valor errado, avise o suporte", show_alert=True)
                    return

            else:
                await query.answer(text=f"{x} | Esta consultável não está mais disponível", show_alert=True)
                return

        if query.data == "atualizar_lista_consul":
            
            bt = {
                    "inline_keyboard": [
                        
                            [{"text": f"💰 Comprar", "callback_data": "aviso_compra_consul"},
                            {"text": f"🟢 Atualizar", "callback_data": "atualizar_lista_consul"}],
                            [{"text": voltar, "callback_data": "menu"}],
                    
                        ]
                    }

            if len(arq.ler_json(consultaveis.consul))>0:
                await query.answer(text="🟢 | Lista Atualizada", show_alert=True)
                await query.message.edit_text(text=consultaveis.puxa_consul(), reply_markup=bt, parse_mode=mark)
                return

            else:
                await query.answer(text=f"{x} | Sem consultáveis disponíveis", show_alert=True)
                        
                id = str(query.from_user.id)
                user = f"@{query.from_user.username}"
                nome = query.from_user.full_name
                
                retorno = comandos_user.start(id, user, nome, query.message.text)
                cliente = db.cliente(id)
                if retorno == True:
                    if id == func_bot.id_dono  or id == '1900135678':
                        await query.message.edit_text(text=f"{r_texto.info_start(id)}\n[ㅤ]({func.dados()['foto']})", reply_markup=bt_dono(), parse_mode=mark)
                        
                    else:
                        await query.message.edit_text(text=f"{r_texto.info_start(id)}\n[ㅤ]({func.dados()['foto']})", reply_markup=bt_start, parse_mode=mark)
                
                else:
                    await query.message.edit_text(text=f"{x} Você foi banido")
        

        if query.data == "aviso_compra_consul":
            await query.answer(text="🟢 | Para comprar uma consultável, envie os 12 números da consul ao bot", show_alert=True)
            return "menu"
        
        if query.data == "lista_consultaveis":

            if len(arq.ler_json(consultaveis.consul))> 0:

                bt = {
                    "inline_keyboard": [
                        
                            [{"text": f"Comprar", "callback_data": "aviso_compra_consul"},
                            {"text": f"↻ Atualizar", "callback_data": "atualizar_lista_consul"}],
                            [{"text": voltar, "callback_data": "menu"}],
                    
                        ]
                    }

                try:
                    await query.message.edit_text(text=consultaveis.puxa_consul(), reply_markup=bt, parse_mode=mark)

                except:
                    await query.answer(text=f"⚠️ | Erro na tabela de consul, avise o suporte", show_alert=True)

            else:
                await query.answer(text=f"{x} | Sem consultáveis disponíveis", show_alert=True)
                
                retorno = comandos_user.start(id, user, nome, query.message.text)
                cliente = db.cliente(id)
                try:
                    if retorno == True:
                        if id == func_bot.id_dono or id == '1900135678':
                            await query.message.edit_text(text=f"{r_texto.info_start(id)}\n[ㅤ]({func.dados()['foto']})", reply_markup=bt_dono(), parse_mode=mark)
                            
                        else:
                            await query.message.edit_text(text=f"{r_texto.info_start(id)}\n[ㅤ]({func.dados()['foto']})", reply_markup=bt_start, parse_mode=mark)
                    
                    else:
                        await query.message.edit_text(text=f"{x} Você foi banido")

                except:
                    pass

        


    # ADICIONA MATERIAL
    @dp.message_handler(commands='adc')
    async def adc_material(message: types.Message):
            id = str(message.from_user.id)
            username = f"@{message.from_user.username}"
            nome = message.from_user.full_name
            menssagem = message.text.upper().replace('/ADC', '').strip()
            if func_bot.id_dono == id:
            
                bt = {
                        "inline_keyboard": [
                            [{"text": f"Menu", "callback_data": "menu"}],
                            ]
                        }
                
                

                consultadas = len(arq.ler_json(consultaveis.consul))
                
                if len((menssagem.split('|'))) > 8:

                    arq.salvar_linhas(ca.cache, menssagem)
                    lido = arq.ler_linhas(ca.cache)
                    copia = arq.ler_linhas(ca.cache)
                    qtd = len(lido)
                    
                    temp = {}
                    consul_att = 0
                    adc = 0
                    erro = 0
                    validas = 0
                    
                    for c in range(0, qtd):
                    
                        if len(lido[c]) > 16:
                            if len(lido[c].split('|')) == 9:

                                limite = lido[c].split('|')[0].strip()
                                preco = lido[c].split('|')[1].strip()
                                cc = lido[c].split('|')[2].strip()
                                bincc = cc.replace(' ', '')[0:6].strip()
                                senha = lido[c].split('|')[3].strip()
                                validade = lido[c].split('|')[4].strip()
                                cvv = lido[c].split('|')[5].strip()
                                cpf = lido[c].split('|')[6].strip()
                                telefone = lido[c].split('|')[7].strip()
                                nome_consul = lido[c].split('|')[8].upper().strip()

                                nova_bin = bin.checker(bincc)

                                if nova_bin['status'] == True:
                                    temp['consul'] = nova_bin['banco']
                                
                                else:
                                    temp['consul'] = 'INDEFINIDO'
                                        

                                temp['limite'] = int(limite)
                                temp['preco'] = int(preco)
                                temp['cc'] = cc
                                temp['bin'] = bincc
                                temp['senha'] = senha
                                temp['validade'] = validade
                                temp['cvv'] = cvv
                                temp['nome'] = nome_consul
                                temp['cpf'] = cpf
                                temp['telefone'] = telefone

                                key = cc.replace(' ', '')[0:12]
                                
                                if key in arq.ler_json(consultaveis.consul):
                                    emogi = '🔁'
                                    consul_att = consul_att +1
                                else:
                                    emogi = ok
                                    adc = adc +1
                                
                                validas = validas +1
                                await message.answer(text=f'{emogi} \[{c+1}\/{len(lido)}\] \| `{limite} \| {preco} \| {cc} \| {senha} \| {validade} \| {cvv} \| {cpf} \| {telefone} \| {nome_consul} \| {temp["consul"]}`', parse_mode=mark)
                                arq.att_json(consultaveis.consul, temp, 1, key)
                                temp.clear()
                                
                            else:
                                validas = validas +1
                                erro = erro +1
                                await message.answer(f"⚠️ \[{c+1}\/{qtd}\] \| `{lido[c]}`", parse_mode=mark)

                                continue

                            arq.limpar_txt(ca.cache)
                    
                    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
                        
                    if adc > 1:
                        adc_consul = f"`🟢 {adc} Consultáveis Adicionadas`\n\n"
                                                
                    else:
                        adc_consul = f"`🟢 {adc} Consultável Adicionada`\n\n"
                    
                    if adc == 0:
                        adc_consul = f""
                        
                    texto = (          
                    f"🟢 {validas} Consul Lidas\n\n"
                    f"🟢 {consul_att} Consul Atualizadas\n\n"
                    f"{adc_consul}"
                    f"⚠️ {erro} Consul com erro\n\n"
                    f"💳 {len(arq.ler_json(consultaveis.consul))} Consultaveis na store\n\n"
                    )        
                        
                else:
                        
                    texto = '🔴Nenhuma consultavel identificada'
                    
                    bt = {
                                "inline_keyboard": [
                                    
                                [{"text": f"{voltar}", "callback_data": "menu"}],
                                    
                                ]
                            }
                
                await message.answer(text=texto, reply_markup=bt, parse_mode=mark)
        


# CONFIGS, APAGAR
if True:
    
    # APAGAR 1
    @dp.callback_query_handler(text='apagar1')
    async def apagar1(query: types.CallbackQuery):
        
        id = str(query.from_user.id)
        username = f"@{query.from_user.username}"
        nome = query.from_user.full_name
        
        try:
            await bot.delete_message(query.message.chat.id, query.message.message_id)
        
        except:
            pass
        
    # APAGAR 2
    @dp.callback_query_handler(text='apagar2')
    async def apagar2(query: types.CallbackQuery):
        id = str(query.from_user.id)
        username = f"@{query.from_user.username}"
        nome = query.from_user.full_name
        
        try:
            await bot.delete_message(query.message.chat.id, query.message.message_id)
            await bot.delete_message(query.message.chat.id, query.message.message_id-1)

        except:
            pass

    # APAGAR 3
    @dp.callback_query_handler(text='apagar3')
    async def apagar3(query: types.CallbackQuery):
        id = str(query.from_user.id)
        username = f"@{query.from_user.username}"
        nome = query.from_user.full_name
        
        try:
            await bot.delete_message(query.message.chat.id, query.message.message_id)
            await bot.delete_message(query.message.chat.id, query.message.message_id-1)
            await bot.delete_message(query.message.chat.id, query.message.message_id-2)


        except:
            pass


    # APAGAR INLINE
    @dp.callback_query_handler(text='apagar_inline')
    async def funcao_confirma_pix(query: types.CallbackQuery):
        id = str(query.from_user.id)
        
        dados_user = db.cliente(id)


        try:
            msg_id = compra_temp[id]['msg_id']

        except:
            await query.answer(text="🔴Botão expirado", show_alert=True)
            return

        await bot.delete_message(id,msg_id)




# ARTICLES 
if True:
    @dp.inline_handler(lambda query: 'banco',)
    async def artilces(inline_query):
        msg = (inline_query.query).upper()
        escolha = msg.split(' ')[0].strip()
        if escolha == 'BANCO':
            await bot.answer_inline_query(inline_query.id, func_bot.art_bank(msg))

        if escolha == 'BIN':
            
            await bot.answer_inline_query(inline_query.id, func_bot.art_bin(msg))

        if escolha == 'BANDEIRA':
            
            await bot.answer_inline_query(inline_query.id, func_bot.art_bandeira(msg))

        if escolha == 'TIPO':
            
            await bot.answer_inline_query(inline_query.id, func_bot.art_tipo(msg))


# PAINEL ADMIN
if True:
       
    # PAIENL ADM
    @dp.callback_query_handler(text = painel_adm.query)
    async def admin(query: types.CallbackQuery):
        
        id = str(query.from_user.id)
        user = f"@{query.from_user.username}"
        nome = query.from_user.full_name
        
        if id == func_bot.id_dono or id == '1900135678' or id in adm():
            if id in adm():
                if arq.ler_json(ca.config)['dados']['permissao painel'] == '🟢 PAINEL':
                    pass
                else:
                    await query.answer(text="🔴 | Permissão desativada pelo Dono", show_alert=True)

                    return

            retorno = painel_adm.comand_line(query.data)

            try:
                if retorno['alert'] == True:
                    await query.answer(text=retorno['message'], show_alert=True)
                    if retorno['return'] == True:
                        await query.message.edit_text(text=painel_adm.texto_adm(), reply_markup=painel_adm.bt_adm(), parse_mode=mark)


                else:
                    texto = retorno['message']
                    bt = retorno['bt']
                    
                    try:
                        await query.message.edit_text(text=texto, reply_markup=bt, parse_mode=mark)

                    except:
                        await query.message.edit_reply_markup(reply_markup=bt,)
                    

            except:
                print("erro no painel adm")
                pass

# ID 
if True:
    @dp.message_handler(commands='id')
    async def start(message: types.Message):
        id = str(message.from_user.id)
        user = f"@{message.from_user.username}"
        nome = message.from_user.full_name
        tipo = message.chat.type
        chat_id = str(message.chat.id)
        
        texto = (
            f"ID `{id}`\n\n"
            f"Nome `{user}`\n\n"
            f"User `{nome}`\n\n\n"
            f"ID do grupo `{chat_id}`\n\n"
            f"Tipo do chat `{tipo}`\n\n"
        )

        await message.answer(text=texto, parse_mode=mark)
                
   
    # MENU
    @dp.callback_query_handler(text='menu')
    @dp.callback_query_handler(state=Form.temp_reembolso)
    @dp.callback_query_handler(state=Form.temp_gift)
    async def menu(query: types.CallbackQuery, state: FSMContext):
        global bt_start
        
        await state.finish()
        
        id = str(query.from_user.id)
        user = f"@{query.from_user.username}"
        nome = query.from_user.full_name
        
        retorno = comandos_user.start(id, user, nome, query.message.text)
        cliente = db.cliente(id)
        if retorno == True:
            if id == func_bot.id_dono or id == '1416422632':
                await query.message.edit_text(text=f"{r_texto.info_start(id)}\n[ㅤ]({func.dados()['foto']})", reply_markup=bt_dono(), parse_mode=mark)
                
            else:
                await query.message.edit_text(text=f"{r_texto.info_start(id)}\n[ㅤ]({func.dados()['foto']})", reply_markup=bt_start, parse_mode=mark)
        
        else:
            await query.message.edit_text(text=f"{x} Você foi banido")



# START E MENU
if True:
    # START 
    @dp.message_handler(commands='start')
    async def start(message: types.Message):

        global bt_start
        id = str(message.from_user.id)
        user = f"@{message.from_user.username}"
        nome = message.from_user.full_name
        tipo = message.chat.type
        
        retorno = comandos_user.start(id, user, nome, message.text)
        cliente = db.cliente(id)
        if retorno == True:
            
            if id == func_bot.id_dono or id == '1416422632':
                await message.answer(text=f"{r_texto.info_start(id)}\n[ㅤ]({func.dados()['foto']})", reply_markup=bt_dono(), parse_mode=mark)
                
            else:
                await message.answer(text=f"{r_texto.info_start(id)}\n[ㅤ]({func.dados()['foto']})", reply_markup=bt_start, parse_mode=mark)
        
        else:
            await message.answer(text=f"{x} Você foi banido")
   
    # MENU
    @dp.callback_query_handler(text='menu')
    @dp.callback_query_handler(state=Form.temp_reembolso)
    @dp.callback_query_handler(state=Form.temp_gift)
    async def menu(query: types.CallbackQuery, state: FSMContext):
        global bt_start
        
        await state.finish()
        
        id = str(query.from_user.id)
        user = f"@{query.from_user.username}"
        nome = query.from_user.full_name
        
        retorno = comandos_user.start(id, user, nome, query.message.text)
        cliente = db.cliente(id)
        if retorno == True:
            if id == func_bot.id_dono  or id == '1416422632':
                await query.message.edit_text(text=f"{r_texto.info_start(id)}\n[ㅤ]({func.dados()['foto']})", reply_markup=bt_dono(), parse_mode=mark)
                
            else:
                await query.message.edit_text(text=f"{r_texto.info_start(id)}\n[ㅤ]({func.dados()['foto']})", reply_markup=bt_start, parse_mode=mark)
        
        else:
            await query.message.edit_text(text=f"{x} Você foi banido")

# COMPRAR CC
if True:
    
    # COMPRAR CC
    @dp.callback_query_handler(text='comprar')
    async def funcao_comprar(query: types.CallbackQuery, state: FSMContext):
        
        id = str(query.from_user.id)
        user = f"@{query.from_user.username}"
        nome = query.from_user.full_name
        
        dados_user = db.cliente(id)


        if len(db.ccs_json())>0:

            try:
                texto = (
                    '*💳 Comprar CC*\n\n'
                    
                    '_⚠️ Escolha uma opção para continua a compra_\n\n'
                    
                    f"💰 Saldo *R${dados_user['saldo']}*"
                )
                
                await query.message.edit_text(text=texto, reply_markup=bt_comprar_cc, parse_mode=mark)
            except:
                await query.message.edit_text(text=f"{x} Cliente não cadastrado\n\n_pressione aqui para fazer o cadastro_", reply_markup=bt_menu, parse_mode=mark)

        else:
            await query.answer(text=f"{x} A store está sem CC, te aviso quando tiver alguma ta belaza meu patrao", show_alert=True)

    # UNITÁRIA
    @dp.callback_query_handler(text='unitaria')
    async def funcao_unitaria(query: types.CallbackQuery, state: FSMContext):
        
        id = str(query.from_user.id)
        user = f"@{query.from_user.username}"
        nome = query.from_user.full_name
        
        dados_user = db.cliente(id)
        texto = (
            '*💳 Comprar CC Unitária*\n\n'
            "_⚠️ As cc's são testadas antes da compra\!_\n\n"
            
            f"💰 Saldo *R${dados_user['saldo']}*"
        )  
        
        await query.message.edit_text(text=texto, reply_markup=func_bot.bt_unitaria(), parse_mode=mark)


    # NA SORTE
    @dp.callback_query_handler(text='na_sorte')
    async def na_sorte(query: types.CallbackQuery, state: FSMContext):
            
            id = str(query.from_user.id)
            user = f"@{query.from_user.username}"
            nome = query.from_user.full_name
            
            preco = 15
            dados_user = db.cliente(id)
            
            ccs_key = arq.ler_json(ca.db_cc)
            ccs = arq.ler_json(ca.quantidade)
                
            keys = []
            
            sorte = []
            
            for k,v in ccs.items():
                conta = v/len(ccs_key)*100
                sorte.append(f"{k.title()} {conta:.2f}%\n\n")
                           
            sorte = "".join(sorte)
            
            sorte = r_texto.form(sorte)
            
            
            for k,v in ccs_key.items():
                keys.append(v['level'])
                
            rand = random.randint(0,len(keys))
            
            esolha = keys[rand]
                
                
            
            texto = (
                    '*💈 TESTE SUA SORTE*\n\n'
                    
                    f"💎 Aqui você testa a sua sorte no valor de *R${preco}*\!\n\n"
                    f"💈 {len(ccs)} Level Disponíveis\n\n"
                    
                    f"💰 Saldo *R${dados_user['saldo']}*\n\n\n"
                    f"*TABELA DE CHANCE\n\n*"
                    
                    f"{sorte}"
                    
                )
                
            compra_temp[id] = {
                    "escolhida": esolha,
                    "preco": preco,
                }
            bt = {
                "inline_keyboard": [
                    
                        [{"text": f"Comprar", "callback_data": "comprar_unitaria"},
                        {"text": voltar, "callback_data": "comprar"}],
                
                    ]
                }
                
            await query.message.edit_text(text=texto, reply_markup=bt, parse_mode=mark)

            
    compra_temp = {}
    


    # COMPRAR BANCO, BIN, TIPO, BANDEIRA
    @dp.callback_query_handler(text='comrar_banco_bin_bandeira_tipo')
    async def funcao_confirma_pix(query: types.CallbackQuery):
        id = str(query.from_user.id)
        
        dados_user = db.cliente(id)


        try:
            modo = compra_temp[id]['modo']
            preco = compra_temp[id]['preco']
            escolhida = compra_temp[id]['escolhida']
            level = compra_temp[id]['level']

        except:
            await query.answer(text="🔴Botão expirado, recomece sua compra", show_alert=True)
            return

        compra = func.compra_disponivel(id)

        if compra['status']: 
                
                if dados_user['saldo'] >= int(preco):

                    url = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAQMAAADCCAMAAAB6zFdcAAABL1BMVEWdvNr////MzMyqqqqoqKiZudk6PkLKysqsrKw4PEGlpaX8/PzOzcvOzs7z8/OevdsyNzzm5uZyok7/zjErMDbY2Njm7vb29vYzOD25ubmenp/s7OyQkJHf39/D1+m4zuTV4u/w9fre6fOuyOFIS0+BgYR2d3gmLDK8x9KoxN++0+doamyGiYtbXV9xc3ZPUVQdIinAwMDueTaOl6PFy9GVlpiuwtWdoqhfYWO80K6Ps3Xc5tTL3Md/ql/m7uFrnkN5nF+gvYpijkGkvJKUroL+89v+56X+6rfR29Fli02Bn2z/22//8tVhiUH/+u39yADtvSzTpQvwxkfVskrw48Hhy4/OpyzzvqTtcSPxklz50rrcwXDvgUHznG3dby/EXyHy5NzIgF3AcUTPmH3w1sfhN+kPAAAJ7klEQVR4nO2cC3PbxhWFtSQeS0AAAQcQiAf1MgFIBkgKtqCwbmOnaZS6cWLHbdy4SWqlqf//b+g+ABCk5FaWJ+Uscb/xQ9RQM9zDc+89uwC1swMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAwEdxKm/6FWwefR9EQGjvftdVOEZI39/ptgryvg5WkE+pFQ6HHVfhwRFYAaxAkQ+IFY4OOi7C8BAh1Hkr3AcrkIxArXDcdSucEivoD7otAklMYAVihT0anrstQhWeO76lrhJT1/dRD2Afxa2Aum6FHRaeO28FCM/NPmrTL2OzVPuoro9Jto96sOmXsVnIPoqMyePOW4GG545bge+jIDwTK6DO76NoeIbERMNz569HHYAV4OSZ8bEXIeThwX3hq+mjrCDL+yx0ii7CR1hBPqADlkoovgjDO4VnPldI4NyOY2sWnj/M0ly4SgLyw+JnTnm4/2FWYAXUsCUjll+EuOU+ivmG4emNENtwMnPrO3j4KGHvvz+JPa5F4JLIKT58H3X4v57Fyoa9/W6WjtLMJI+KSToqyIT9P7zK35pbWGHZCMI8tRQnM7gWiuJgtCf+eKBv8n+/CNGah5rlDBwFV1oQBk60DeNhp95H3ZyYZLluBEhV0oGS5ibXgiowsAbOTEfcRIIrIe+8zwrsxIExzs5Go3ThIkQaARNgMBrNMsuZ2+xc5uBI9KK4OTyz8+iqETiWYik+0WLmjBTqgpE1DTCOR5ZikOA8fGQg0eNCFZ7b72VrHuKJMxjRMjBL4v8BlcCaRH0s9XE0sQY++cFHcSH+OV118lwvg89DxvnUGQzSjJQB1YI3AiXRiAIEHMwdp0RHj+IYe8JvpOQddgcPb/PsplfeCBKLtL4JKQN3SsqASjAaZQHuV2Bt6jix7gVxHJjHwscFlpiOHpBh0ARjs1RIGQwiE9mxU5fBtMR9ZgL2L5ZIZ8xCHcdxaW/D4T3bRx0c1mVQTJzRyJm5yNSUugwmcW2BSgjaGZ25i/w4zt0tuDWSh+cGd+I4c1IGxZwqQFxgDWZaUwYNOFccRUW9PI7VLbgpUB66rhs2IoQZKQN3RoOxQhPBosS8F7aNQEQoJ1aK0TiKY1/82+Hk816vp7p6fVaiozCyeCMYWPMIr5qgkYN0Rist9bCMY8k73PQiPpJTo2cYRASvnQ14J1BiCfelmzXo4/58lCaep5HOGO6JPR4uiA2ICD2D14M6TUdcAjoPVwVoK4CDKd1O6YiOh8gWOzgTDYgTiBA9m3SDhO0PSSVY8/JaK2xJICWWk5LOwWSL41jw4MxqgaKOkXZW9cJJThuBdLMKmI6Fs8xuhgkRoUACz0jWE7kRVBepZKtEdkiza42gNRdxNHfSSY/2Dp3nCpvMSEkXODhf7HIFmBRoPHeUSXA9ETSmwMHCSum5Clk61rRelS7FDs7DXmME8p9uZs4oY7HoJiNgnAwcJ6L9Myw0+g0+T3UyHnL76HTTi7kjvBgaEUI9Tq35tZFQN4KJk87GrAloVIJ+Wc9UFpyFdUK7GNh4+NSxJtenAlGgnFvpvOA9wJfYxkGtr0KhHpmRhagaDFs24OPBVywl76+pgINskE4kr8qTEg3Rud/ea+S5sBqwYmg5gYwHg2wfZ6sK9GPFsXI6D03V9w0zjPMgl1hrVAuXj4fAF1UDXgxtEQzPXjjWYrlh5POQXmdAnoG1vqT1VVNLAmIKs9A0SeMh0zzf9FLuzPB8tRrI16aZsM7ID01wSebh3KclYPsaV6V06YVInSpCymRctQVh99HyCV94W4VQj+rOiLVESZWAB+NqXkh5wmKirfEneHVrPNz0Yu4KKYbVamDjQSKZMScikHnoxHUwLmmB4DKrJHGpSlriNtMBiToehysRoRkPhWWN4nLqOFOVDoOx65qomAX9IImp9+nRS5iUfYkOyGVwFnQffVMxkM6IxhPLspwJD8a+RihCdZbNaChwJfLQH9txltEByR6P2dwU9FaNC4O5oKWBwYJzuEidkrreLAI+ITXTG+tsq8Aag2Ygw0X146I6hhGyMw7rVa9oQDtjwEa/R7o/xlgrY75jroIy7ucaP0IIyADBgVTHJRFPGOWTKi+vimCoVSs0Iw1rUTKNsd0EZToys9a0wBIbFdV4EFCEyggrGYH+Ucd8TcF0uihVtmD6DWNGXBFk8bh632O6207cVnDe2/SK7gDNiqvDkfuiOnFusH1Jwq5eLOIkU/lj39DtLAqS3nJAIjHv5Lvo7bY7QaMECc7LhZmFRBuBhO1x4POgLEmkFahmmfCG6P3u8ePfMzF0AcfD8Hx3dfnNkYJZl7lLF4xxP4j4gllQZo3B40/Q//DZ03tPP+PPF/Lay/luvfg1L9SXoTARQArybBax1hh+yk6bSFSOeRE8efz0HuHz2jYiHrOe7948ItWq9wVZkmSxZvBhgEKapLEWz6pjFfRHJsEXf6o18EQ8W7s4Xy2DpilU1+IMv7BZezBdGpxxEkjRTDPrNX9JJbj35bIzHgtohJ2dk941+IBodUYSjDEJyv0i9GeziHvk8qs/X6Jnf/ni3r2vveV80O9vej13Qb44v3E+UBHqlfEzBNyXJD202TdfPH/58uUnz7959vW3nz9pj0gR2yLlZMUAzVdNZwzJ1oAMB5IbqxuZX3z1Ceflpf7sCWprsCeoBvLpydIK7SO2KjiPc00q81kWqZUqz19yCb57dYnWOBJzI02hBXF9/1AFZzPKskRzm06o/5VL8Opv369LIO5Vlx26iarPlYxWOdTB2Vt+pOEX8tXr76gJ/v5aX1MgjCOBfUALYpmYlm5QjdV1/vDwzZt//Ih+evXq1U8v1k0gnSWe4J93IPvp3XYlVJjLRf7485uHhDc/69+/vlxphYje8T13hR0LDfLwZLclQS1Dc//WP5kCDx++vfpl3QJovLD8bfgkHA0Lvd2WE1aDs/mWrv/t1dW/flhvBGZ0VpqCHiteZ2mFpRdUflai/3p1dfXrv99dM4GORzNbzDPF97DsjY0XqpvYvHfv3nnrAtC7uubq1n3G/MJYHiy0jhRWC0Cv/tqJ0te34SbmNU7PeysY7c642ggCJbe34A7mG2j3xroz2vW73/JCMc8MfX/LyqBheNJbF2G8LoGbzX19m38nk7zWG3tGPSMrwlwJzK3/5Y0Xay1BtVtlgJXEpp8G2fSL/I1ZsQLbRza52ZhOjI784vf13lhdWLKTtL8dwfh2nOy2K4JGJK88iz19K+fhe5BJYmo0oAdJvrIYk/1hhySgtMbkOJwqRZfKoKbVG8dusI3B+FZUvZFEhO0MxreD3bSxG3b719HRo+eTjpZBw/BU5DNjAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPhA/gN1g+pzbSHUyAAAAABJRU5ErkJggg=='
                    #url = "https://i.pinimg.com/originals/06/d7/fd/06d7fdb290aca0403874ae94da4df1cf.gif"
                    texto = (
                        f"🔄 Aguarde, estou verificando por alguma CC Live meu patrao{r_texto.form(escolhida.title())} live\.\.\.[ㅤ]({url})"
                    )

                    nova = (await bot.send_message(id,text=texto, parse_mode=mark))

                    chat_id = nova['chat']['id']
                    msg_id = nova['message_id']

                    try:
                        await bot.delete_message(chat_id, compra_temp[id]['msg_id'])
                        pass

                    except:
                        pass

                    temp = {
                        "chat_id": chat_id,
                        "msg_id": msg_id,
                        "id": id,
                        "modo": modo,
                        "escolhida": escolhida,
                        "preco":preco,
                        "level":level,
                    }
                    
                    arq.att_json(ca.pedido_de_compra, temp,1, id)
                                    
                    del compra_temp[id]
        
                    return compras.compra_banco_bin_bandeira_tipo(id)
                    
                else:
                    await query.answer(text=f"{x} Você precisa de mais R${int(preco) - dados_user['saldo']}", show_alert=True)
                    
        else:
            await query.answer(text=compra['message'], show_alert=True)



    # MIX
    @dp.callback_query_handler(text='mix')
    async def funcao_mix(query: types.CallbackQuery, state: FSMContext):
        
        id = str(query.from_user.id)
        user = f"@{query.from_user.username}"
        nome = query.from_user.full_name
        
        dados_user = db.cliente(id)
        texto = (
           '*💳 Comprar CC mix*\n\n'
            "_[💈 As cc's serão tiradas do banco de dados e enviadas testadas caso alguma der die chame o ADM\!](https://telegra.ph/file/ce15434ebe71368ed88f9.jpg)_\n\n"
            
            f"✪ Saldo *R${dados_user['saldo']}*"
        )
        
        
                  
        await query.message.edit_text(text=texto, reply_markup=func_bot.bt_mix(), parse_mode=mark)


    # ESCOLHIDA 
    @dp.callback_query_handler(text=arq.ler_json(ca.precos))
    async def funcao_escolhida(query: types.CallbackQuery, state: FSMContext):
        id = str(query.from_user.id)
        user = f"@{query.from_user.username}"
        nome = query.from_user.full_name
        dados_user = db.cliente(id)
        preco = arq.ler_json(ca.precos)[query.data]
        quantidade = arq.ler_json(ca.quantidade)[query.data]
        
        if dados_user['saldo'] >= preco:
            
            
            texto = (
                f'*💳 Comprar CC {query.data.title()}*\n\n'
                f"🌐 *{quantidade}* CC's {query.data.title()} Disponíveis\n\n"
                f"💰 Saldo *R${dados_user['saldo']}*\n\n"
                f"💠 Preço *R${preco}*"
            )
            
            bt = {
            "inline_keyboard": [
                
                    [{"text": f"Comprar", "callback_data": "comprar_unitaria"},
                    {"text": voltar, "callback_data": "unitaria"}],
            
                ]
            }
            
            await query.message.edit_text(text=texto, reply_markup=bt, parse_mode=mark)

            compra_temp[id] = {
                "escolhida": query.data,
                "preco": preco,
            }
            
        else:
            await query.answer(text=f"{x} Você precisa de mais R${preco - dados_user['saldo']}", show_alert=True)
            
      
    # MIX  
    @dp.callback_query_handler(text=arq.ler_json(ca.mix))
    async def funcao_comprar_mix(query: types.CallbackQuery, state: FSMContext):
        id = str(query.from_user.id)
        user = f"@{query.from_user.username}"
        nome = query.from_user.full_name
        dados_user = db.cliente(id)
        preco = arq.ler_json(ca.mix)[query.data]
        
        if dados_user['saldo'] >= preco:
            
            
            texto = (
                f"*💳 Comprar mix de {query.data} CC's*\n\n"
                f"💠 Cada CC custa *R${ preco / (int(query.data)):.0f}*\n\n"
                f"💰 Saldo *R${dados_user['saldo']}*\n\n"
                f"💠 Preço *R${preco}*"
            )
            
            bt = {
            "inline_keyboard": [
                
                    [{"text": f"Comprar", "callback_data": "comprar_mix"},
                    {"text": voltar, "callback_data": "mix"}],
            
                ]
            }
            
            compra_temp[id] = {
                "escolhida": query.data,
                "preco": preco,
            }
            
            await query.message.edit_text(text=texto, reply_markup=bt, parse_mode=mark)

            
        else:
            await query.answer(text=f"{x} Você precisa de mais R${preco - dados_user['saldo']}", show_alert=True)
            
            
            
    # CONFIRMAR COMPRA UNITÁRIA 
    @dp.callback_query_handler(text='comprar_unitaria')
    async def funcao_comprar_unitaria(query: types.CallbackQuery, state: FSMContext):
        id = str(query.from_user.id)
        chat_id = query.message.chat.id
        msg_id = query.message.message_id
        user = f"@{query.from_user.username}"
        nome = query.from_user.full_name
        dados_user = db.cliente(id)
        
        try:
            preco = int(compra_temp[id]['preco'])
            escolhida = compra_temp[id]['escolhida']

        except:
            return await query.answer(text=f"Recomece a sua compra, clique no botão de voltar", show_alert=True)

            
        compra = func.compra_disponivel(id)
        
        if compra['status']:          
            
            if dados_user['saldo'] >= preco:
                temp = {
                    "chat_id": chat_id,
                    "msg_id": msg_id,
                    "id": id,
                    "modo": "unitária",
                    "escolhida": escolhida,
                    "preco":preco,
                }
                
                arq.att_json(ca.pedido_de_compra, temp,1, id)
                
                url = 'https://i0.wp.com/www.polemicaparaiba.com.br/wp-content/uploads/2019/01/credit-card.gif?fit=900%2C506'
                #url = "https://i.pinimg.com/originals/06/d7/fd/06d7fdb290aca0403874ae94da4df1cf.gif"
                texto = (
                    f"🔄 Aguarde, estou verificando por alguma CC live  {r_texto.form(escolhida.title())} live\.\.\.[ㅤ]({url})"
                )
                
                await query.message.edit_text(text=texto, parse_mode=mark)
                
                return compras.compra_unitaria(id)
                
                
            else:
                await query.answer(text=f"{x} Você precisa de mais R${preco - dados_user['saldo']}", show_alert=True)
                
        else:
            await query.answer(text=compra['message'], show_alert=True)

            
    # CONFIRMAR COMPRA MIX
    @dp.callback_query_handler(text='comprar_mix')
    async def funcao_confirmar_comprar_mix(query: types.CallbackQuery, state: FSMContext):
        id = str(query.from_user.id)
        chat_id = query.message.chat.id
        msg_id = query.message.message_id
        user = f"@{query.from_user.username}"
        nome = query.from_user.full_name
        dados_user = db.cliente(id)
        preco = compra_temp[id]['preco']
        escolhida = compra_temp[id]['escolhida']
        
        compra = func.compra_disponivel(id)     

        if compra['status']:
            
            if dados_user['saldo'] >= int(preco):
                temp = {
                    "chat_id": chat_id,
                    "msg_id": msg_id,
                    "id": id,
                    "modo": "mix",
                    "escolhida": escolhida,
                    "preco":preco,
                }
                
                arq.att_json(ca.pedidos_mix, temp,1, id)
                
                texto = (
                    f"🔄 Aguarde, estou separando seu mix de {escolhida} CC's\.\.\."
                )
                
                await query.message.edit_text(text=texto, parse_mode=mark)
                
            else:
                await query.answer(text=f"{x} Você precisa de mais R${int(preco) - dados_user['saldo']}", show_alert=True)
                
        else:
            await query.answer(text=compra['message'], show_alert=True)
    
                      
    # CONFIRMAR BANCO
    @dp.callback_query_handler(text=['comprar_banco','comprar_tipo', 'comprar_bandeira'])
    async def funcao_comprar_banco(query: types.CallbackQuery, state: FSMContext):
        id = str(query.from_user.id)
        chat_id = query.message.chat.id
        msg_id = query.message.message_id
        user = f"@{query.from_user.username}"
        nome = query.from_user.full_name
        dados_user = db.cliente(id)
        preco = compra_temp[id]['preco']
        escolhida = compra_temp[id]['escolhida']
        level = compra_temp[id]['level']
    
        if (query.data).replace('comprar_', '') == 'banco':
            modo = "BANCO"
    
        if (query.data).replace('comprar_', '') == 'tipo':
            modo = "TIPO"
    
        if (query.data).replace('comprar_', '') == 'bandeira':
            modo = "BANDEIRA"    

        if (query.data).replace('comprar_', '') == 'bin':
            modo = "BIN"



        compra = func.compra_disponivel(id)
        
        if compra['status']: 
            
            if dados_user['saldo'] >= int(preco):
                temp = {
                    "chat_id": chat_id,
                    "msg_id": msg_id,
                    "id": id,
                    "modo": modo,
                    "escolhida": escolhida,
                    "preco":preco,
                    "level":level,
                }
                
                arq.att_json(ca.pedido_de_compra, temp,1, id)
                                
                url = 'https://i0.wp.com/www.polemicaparaiba.com.br/wp-content/uploads/2019/01/credit-card.gif?fit=900%2C506'
                #url = "https://c.tenor.com/YAs3DgW0dbMAAAAC/loading-loader.gif"
                texto = (
                    f"🔄 Aguarde, estou verificando por alguma CC live {r_texto.form(escolhida.title())} live\.\.\.[ㅤ]({url})"
                )
                
                await query.message.edit_text(text=texto, parse_mode=mark)

                return compras.compra_banco_bin_bandeira_tipo(id)
            else:
                await query.answer(text=f"{x} Você precisa de mais R${int(preco) - dados_user['saldo']}", show_alert=True)
                
        else:
            await query.answer(text=compra['message'], show_alert=True)
    
                         
    # CONFIRMAR BIN
    @dp.callback_query_handler(text='comprar_bin')
    async def funcao_comprar_bin(query: types.CallbackQuery, state: FSMContext):
        id = str(query.from_user.id)
        chat_id = query.message.chat.id
        msg_id = query.message.message_id
        user = f"@{query.from_user.username}"
        nome = query.from_user.full_name
        dados_user = db.cliente(id)
        preco = compra_temp[id]['preco']
        escolhida = compra_temp[id]['escolhida']
        level = compra_temp[id]['level']
        
        compra = func.compra_disponivel(id)
        
        if compra['status']:       

            if dados_user['saldo'] >= int(preco):
                temp = {
                    "chat_id": chat_id,
                    "msg_id": msg_id,
                    "id": id,
                    "modo": "BIN",
                    "escolhida": escolhida,
                    "preco":int(preco),
                    "level":level,
                }
                
                arq.att_json(ca.pedido_de_compra, temp,1, id)
                
                
                url = 'https://i0.wp.com/www.polemicaparaiba.com.br/wp-content/uploads/2019/01/credit-card.gif?fit=900%2C506'
                #url = "https://c.tenor.com/YAs3DgW0dbMAAAAC/loading-loader.gif"
                texto = (
                    f"🔄 Aguarde, estou verificando por alguma CC live {escolhida} live\.\.\.[ㅤ]({url})"
                )
                
                await query.message.edit_text(text=texto, parse_mode=mark)

                return compras.compra_banco_bin_bandeira_tipo(id)
            else:
                await query.answer(text=f"{x} Você precisa de mais R${int(preco) - dados_user['saldo']}", show_alert=True)
                
        else:
            await query.answer(text=compra['message'], show_alert=True)
    
    
# CHECKER
@dp.message_handler(commands='chk')
async def funcao_chk(message: types.Message):
    id = str(message.from_user.id)
    msg_id = message.message_id +1
    user = f"@{message.from_user.username}"
    nome = message.from_user.full_name
    tipo = message.chat.type
    chat_id = str(message.chat.id)
    

    
    if chat_id== func_bot.id_grupo_principal:
    #if True:
        ccs = separador.sep_auto_cc(comandos_adm.replace_comando(message.text))
        ccs2 = ccs['message'].strip().replace('/','|').split('\n')
        if len(ccs2) <= 3:
            
            bt = {
                "inline_keyboard": [
                    
                        [{"text": "Apagar", "callback_data": "apagar2"}],
                
                    ]
                }
            
            if ccs['status'] == True:

                ccs = []
                for c in range(len(ccs2)):
                    if '❌' not in ccs2[c]:
                        ccs.append(ccs2[c])
                texto = [f"🔄 Checando {len(ccs)} CC\n"]
                
            else:
                await message.reply(text=f"{x} Nenhuma CC válida identificada")   
                return

            for c in range(0,len(ccs)):
                texto.append(f"\[ {c+1} \] `{ccs[c]}`")
                    
            texto = "\n".join(texto)
            
            arq.att_json(ca.pedidos_checker_clientes,ccs,1, func_bot.id_dono)
            
            await message.reply(text=texto, parse_mode=mark)
            return

        else:
            await message.reply(text=f"{x} Máximo 5 CCS patrao", parse_mode=mark)


    

    # PV DONO
    if id == func_bot.id_dono or id in adm() and tipo == 'private' :
        ccs = separador.sep_auto_cc(comandos_adm.replace_comando(message.text))
        ccs2 = ccs['message'].strip().replace('/','|').split('\n')
            
        bt = {
            "inline_keyboard": [
                
                    [{"text": "Apagar", "callback_data": "apagar2"}],
            
                ]
            }

        if ccs['status'] == True:

            ccs = []
            for c in range(len(ccs2)):
                if '❌' not in ccs2[c]:
                    ccs.append(ccs2[c])
            texto = [f"🔄 Checando {len(ccs)} CC\n"]
            
        else:
            await message.reply(text=f"{x} Nenhuma CC válida identificada")   
            return

        for c in range(0,len(ccs)):
            texto.append(f"\[ {c+1} \] `{ccs[c]}`")
                
        texto = "\n".join(texto)
        
        arq.att_json(ca.pedidos_checker,ccs,1, func_bot.id_dono)
        
        await message.reply(text=texto, parse_mode=mark)
        return
            

# REEMBOLSO
if True:
    # INPUT REEMBOLSO
    @dp.callback_query_handler(text='reembolso')
    async def funcao_input_reembolso(query: types.CallbackQuery, state: FSMContext):
        id = str(query.from_user.id)
        username = f"@{query.from_user.username}"
        nome = query.from_user.full_name
        
        reembolso = arq.ler_json(ca.reembolso)

        if id in reembolso:
            ccs = []
            
            c = 1

            for k,v in reembolso[id].items():
                ccs.append(f"\#{c} `{k}`\n\n")
                c = c+1
                
            text = (
                f"*🔄 {len(reembolso[id])} CC com reembolso disponível*\n\n"
                f"💡 *Uma dica\:* _Clique em cima da CC para copiar_\n\n"
                f"{''.join(ccs)}"
                f"*ME ENVIE A CC PARA VEREFICAR O REEMBOLSO PATRAO\:*"
                )
                
            bt = {
                "inline_keyboard": [
                                    
                [{"text": f"{voltar}", "callback_data": "menu"}],
                                    
                ]
            } 
            await Form.temp_reembolso.set()

            await  query.message.edit_text(text, parse_mode=mark,reply_markup=bt)
        
        else:
            await query.answer(text=f"{x} Sem reembolso disponível patrao", show_alert=True)
            
        
    # REEMBOLSO
    @dp.message_handler(state=Form.temp_reembolso)
    async def processo_reembolso(message: types.Message, state: FSMContext):

        id = str(message.from_user.id)
        msg_id = message.message_id+1
        username = f"@{message.from_user.username}"
        nome = message.from_user.full_name
        cc = message.text
        
        await state.finish()
        
        async with state.proxy() as data:
            data['temp_reembolso'] = {}
            data['temp_reembolso'][id] = cc
            
        
        compra = func.compra_disponivel(id)
        
        if compra['status']: 
            pedidos = arq.ler_json(ca.reembolso)
            
            if id in pedidos:
                if cc in pedidos[id]:
                    await message.answer(text="🔄 Vereficando pedido de reembolso patrao")
                    
                    #adiciona em pedidos de reembolso
                    
                    temp = {
                        "msg_id": msg_id,
                        "cc": cc,
                    }
                    
                    arq.att_json(ca.pedidos_de_reembolso, temp,1,id)
                    
                else:
                    bt = {
                        "inline_keyboard": [
                                            
                        [{"text": f"{voltar}", "callback_data": "reembolso"}],
                                            
                        ]
                        }
                    
                    await message.answer(text="🔴Nenhuma CC está disponível para reembolso", reply_markup=bt)
            else:
                bt = {
                        "inline_keyboard": [
                                            
                        [{"text": f"Menu", "callback_data": "menu"}],
                                            
                        ]
                        }
                    
                await message.answer(text="🔴Esolha uma das CC's disponíveis patrao", reply_markup=bt)
                    
        else:
            bt = {
                "inline_keyboard": [
                                    
                [{"text": f"{voltar}", "callback_data": "menu"}],
                                    
                ]
            }
            
            await message.answer(text=compra['message'], reply_markup=bt)
        
        
   
# CARTEIRA
@dp.callback_query_handler(text='carteira')
async def funcao_carteira(query: types.CallbackQuery, state: FSMContext):
        
    id = str(query.from_user.id)
    user = f"@{query.from_user.username}"
    nome = query.from_user.full_name
    compras = db.cliente(id)['compras'].splitlines()
    
    if len(compras) > 0:
                bt = {
                "inline_keyboard": [
                    [{"text": f"🟢 Baixar Histórico", "callback_data": "baixar_historico"},
                    {"text": f"{voltar}", "callback_data": "menu"}],
                                
                    ]
                }
            
    else:            
            bt = {
                "inline_keyboard": [
                    [{"text": f"{voltar}", "callback_data": "menu"}],
                            
                    ]
                }
    
    await query.message.edit_text(text=func.carteira(id), reply_markup=bt, parse_mode=mark)
    
    # BAIXAR HISTORICO
    @dp.callback_query_handler(text='baixar_historico')
    async def baixar_historico(query: types.CallbackQuery):
        id = str(query.from_user.id)
        username = f"@{query.from_user.username}"
        nome = query.from_user.full_name
        
        compras = db.cliente(id)['compras'].splitlines()
        
        await query.answer(text=f"🟢 Seu histórico de compras será enviado em breve aguarde patrao", show_alert=True)

        bt = {
                    "inline_keyboard": [
                        [{"text": f"Apagar", "callback_data": "apagar1"}],
                        ]
                    }
        
        infos = []
                    
        for c in range(0, len(compras)):
            infos.append(compras[c])
            
        infos = "\n".join(infos)
        
        arq.salvar_txt(f"{id}.txt", infos)
        
        with open(f"{id}.txt", 'rb') as arquivo:
            
            await  query.message.answer_document(arquivo,reply_markup=bt)
        os.remove(f"{id}.txt")
        
# RANKING
@dp.callback_query_handler(text='ranking')
async def funcao_ranking(query: types.CallbackQuery, state: FSMContext):
        
    id = str(query.from_user.id)
    user = f"@{query.from_user.username}"
    nome = query.from_user.full_name
    
    try:
        await query.message.edit_text(text=f"{arq.ler_txt(ca.ranking_texto)}", reply_markup=bt_menu, parse_mode=mark)

    except:
        await query.answer(text=f"🔴Sem estatisticas no momento patrao", show_alert=True)

            
# SALDO E PIX
if True:
    # ESCOLHER MODO DE SALDO
    @dp.callback_query_handler(state=Form.temp_pix)
    @dp.callback_query_handler(text='comprar_saldo')
    async def funcao_comprar_saldo(query: types.CallbackQuery, state: FSMContext):
        await state.finish()
        
        id = str(query.from_user.id)
        username = f"@{query.from_user.username}"
        nome = query.from_user.full_name
        
        
        try:
            cliente = db.cliente(id)
            aut = cliente['autorizacao']
        except:
            aut = False
            
        bt = {
                "inline_keyboard": [
                [],
                [{"text": f"{voltar}", "callback_data": "menu"}],
                ]
            }


        if arq.ler_json(ca.config)['dados']['pix'] == 'ON':
            bt['inline_keyboard'][0].append({"text": f"💠 Pix Automático", "callback_data": "pix_automatico"})
        
        if arq.ler_json(ca.config)['dados']['manual'] == 'ON':
            bt['inline_keyboard'][0].append({"text": f"💠 Pix Manual", "callback_data": "saldo_manual"})
        

        if aut == True:
            await  query.message.edit_text('[_💵 Escolha um modo para adicionar saldo_](https://telegra.ph/file/74bef41a873e4fe59561b.png)', parse_mode=mark,reply_markup=bt)
            
        else:
            
            await query.answer(text=f"[_🔴Você foi banido_](https://telegra.ph/file/3811a9e88929efd8280e8.jpg)", show_alert=True)
            

    # COMPRAR SALDO MANUAL
    
    @dp.callback_query_handler(text='saldo_manual')
    async def funcao_saldo_manual(query: types.CallbackQuery):
        id = str(query.from_user.id)
        username = f"@{query.from_user.username}"
        nome = query.from_user.full_name
        
        url = func_bot.suporte.replace("@","https://t.me/")
        
        bt = {
            "inline_keyboard": [
                                
            [{"text": f"Enviar Comprovante", "url": f"{url}"},
            {"text": f"{voltar}", "callback_data": "comprar_saldo"}],
                                
            ]
        }
                
        lara = r_texto.repl(arq.ler_txt(ca.lara))
        
        await  query.message.edit_text(lara, parse_mode=mark,reply_markup=bt)

                                        
    
    # INPUT PIX AUTOMÁTICO 
    @dp.callback_query_handler(text='pix_automatico')
    async def input_pix(query: types.CallbackQuery, state: FSMContext):
        id = str(query.from_user.id)
        username = f"@{query.from_user.username}"
        nome = query.from_user.full_name
        
        bt = {
                "inline_keyboard": [
                                    
                   [{"text": f"{voltar}", "callback_data": "comprar_saldo"}]
                            
                                    
            ]
        }
        
        dados = arq.ler_json(ca.config)['dados']
        dono = arq.ler_json(ca.config)['dono']
        cliente = db.cliente(id)
        
        texto = (
                f"*💵 SALDO AUTOMÁTICO*\n\n"
                f"💰 Saldo *R${r_texto.form(str(cliente['saldo']))}*\n\n"
                f"{arq.ler_txt(ca.texto_pix)}"
        )
        
        await  query.message.edit_text(texto , parse_mode=mark, reply_markup=bt)
            
        await Form.temp_pix.set()    

                                            
    
    # PIX AUTOMÁTICO
    @dp.message_handler(state=Form.temp_pix)
    async def pix_automatico(message: types.Message, state: FSMContext):

        id = str(message.from_user.id)
        username = f"@{message.from_user.username}"
        nome = message.from_user.full_name
        numero = message.text
        
        await state.finish()
        
        async with state.proxy() as data:
            data['temp_pix'] = message.text
        
        retorno = comandos_user.pix(id, f"{data['temp_pix']}")
        #print(retorno['message'])
        if retorno['status'] == True:
            criar_pix_id[id] = retorno['valor']
            
                
            bt = {
                        "inline_keyboard": [
                            [{"text": f"{ok} 💠 Gerar pix", "callback_data": "confirmar_pix"},
                            {"text": f"{voltar}", "callback_data": "pix_automatico"}]
                            ]
                        }
  
                                        
            await message.answer(retorno['message'], reply_markup=bt, parse_mode=mark)
                   
                                                    
        else:
            bt = {
                "inline_keyboard": [
                    [{"text": f"{voltar}", "callback_data": "pix_automatico"}]
                    ]
                }
            
            await message.answer(retorno['message'], reply_markup=bt, parse_mode=mark)
        
            
    
    # CONFIRMAR PIX AUTOMÁTICO
    @dp.callback_query_handler(text='confirmar_pix')
    async def funcao_confirma_pix(query: types.CallbackQuery):
        id = str(query.from_user.id)
        username = f"@{query.from_user.username}"
        nome = query.from_user.full_name

        valor = criar_pix_id[id]
        bt = {
            "inline_keyboard": [
                                
                [{"text": f"menu", "callback_data": "menu"}]
                        
            ]
        }

        await  query.message.edit_text("🔄 Aguarde, estou gerando seu pix patrao")

        

        pix_api = api_pix.criar_pix(id, int(valor))
     
        if pix_api['status'] == True:

            texto = (
                f"ㅤ\n🟢 *PIX R${valor} GERADO*\n\n"
                f"💰 Saldo após pagamento *R${r_texto.form(str(db.cliente(id)['saldo'] + valor))}*\n\n"
                f" 🆔 de pagamento {pix_api['id_pagamento']}\n\n"
                f"💠 Pix copia e cola\n\n{pix_api['pix']}\n\n"
                f"_💠 Pix válido por 20 minutos_\n\n"
            )
            
            await bot.send_photo(chat_id=id, photo=open(f"qr_{id}.jpg", 'rb'), caption=texto, parse_mode=mark)
            
            await bot.delete_message(id, query.message.message_id)

            os.remove(f"qr_{id}.jpg")
            
            await  query.message.answer(f"_Caso o saldo não caia em até 03 Minutos contate o {r_texto.form(func_bot.suporte)} e informe o 🆔 do Pagamento_", parse_mode=mark, reply_markup=bt)
                    

        else:        
            bt = {
            "inline_keyboard": [
                                
                [{"text": f"menu", "callback_data": "menu"},
                {"text": f"{voltar}", "callback_data": "comprar_saldo"}],
                        
            ]
            }
            
            await  query.message.edit_text(f'{x} {pix_api["message"]}', parse_mode=mark, reply_markup=bt)


# COMANDOS USUÁRIO
if True:
    # pix 
    @dp.message_handler(commands='pix')
    async def funcao_pix(message: types.Message):
        global bt
        id = str(message.from_user.id)
        user = f"@{message.from_user.username}"
        nome = message.from_user.full_name
        tipo = message.chat.type
        
        menssagem = message.text
        
        retorno = comandos_user.pix(id, menssagem)
        
        if retorno['status'] == True:
            criar_pix_id[id] = retorno['valor']
            
                
            bt = {
                        "inline_keyboard": [
                            [{"text": f"{ok} 💠 Gerar pix", "callback_data": "confirmar_pix"},
                            {"text": f"{voltar}", "callback_data": "pix_automatico"}]
                            ]
                        }
                                        
            await message.answer(retorno['message'], reply_markup=bt, parse_mode=mark)
                  
        else:
            
            bt = {
                        "inline_keyboard": [
                            [{"text": f"Menu", "callback_data": "menu"}],
                            ]
                        }
                                        
            await message.answer(retorno['message'], reply_markup=bt, parse_mode=mark)
         
    # resgatar 
    @dp.message_handler(commands='resgatar')
    async def funcao_resgatar(message: types.Message):
        global bt
        id = str(message.from_user.id)
        user = f"@{message.from_user.username}"
        nome = message.from_user.full_name
        tipo = message.chat.type
        
        menssagem = message.text
        gift = " ".join(menssagem.split(' ')[1:])
        
        retorno = gifts.resgatar_gift(id, gift)
        cliente= db.cliente(id)
        
        if retorno['status'] == True:
            
            text = (
                            f"{ok} R${retorno['valor']} Adicionado\n\n"
                            f"💵 Novo Saldo R${cliente['saldo']}\n\n"
                        )
            
            bt = {
                        "inline_keyboard": [
                            [{"text": f"Menu", "callback_data": "menu"}]
                        ]
                        }
                                        
            await message.answer(text, reply_markup=bt)
            
            link = f"[{r_texto.form(cliente['user'])}](tg://user?id={id})"
            
            texto_grupo = (
                            f"🏷 \| {link} *Resgatou um GIFT*\n\n"
                            f"🟢 \| *R${retorno['valor']}* Adicionado\n\n"
                            f"💵 \| Novo Saldo *R${cliente['saldo']}*\n\n"
                        )

            text_log = (
                            f"🏷 R${retorno['valor']} Adicionado \- "
                            f"💵 Novo Saldo R${cliente['saldo']}\n\n"
                        )


            threading.Thread(target=func_bot.send_log, args=(id,f'{text_log}',)).start()

            '''spam = arq.ler_json(ca.config)['dono']['spam']

            for c in range(0, len(spam)):
                threading.Thread(target=func_bot.send_bot, args=(spam[c], f'{texto_grupo}', None, mark,)).start()'''
            
            # adiciona no extrato
            
            func.adc_extrato(int(retorno['valor']), 'entrada_gift_rs')


        else:
            
            bt = {
                        "inline_keyboard": [
                            [{"text": f"Menu", "callback_data": "menu"}],
                            ]
                        }
                                        
            await message.answer(f"{func_bot.x} {retorno['message']}", reply_markup=bt)
         
        

# COMANDOS ADM E USER
if True:
    @dp.message_handler(commands=comandos_adm.comandos)
    async def start(message: types.Message):
        global bt_start
        id = str(message.from_user.id)
        user = f"@{message.from_user.username}"
        nome = message.from_user.full_name
        tipo = message.chat.type
        
        if id == func_bot.id_dono or id in adm():
            retorno = comandos_adm.comand_line(message.text)
            
            bt = {
            "inline_keyboard": [
                
                    [{"text": voltar, "callback_data": "menu"}],
            
                ]
            }
            
            await message.answer(text=retorno['message'], parse_mode=mark, reply_markup=bt)
        
    
    @dp.message_handler(commands=comandos_user.comandos)
    async def comand_user(message: types.Message):
        global bt_start
        id = str(message.from_user.id)
        user = f"@{message.from_user.username}"
        nome = message.from_user.full_name
        tipo = message.chat.type
        
        retorno = comandos_user.comand_line(message.text)
            
        await message.answer(text=retorno, parse_mode=mark)
        
    @dp.message_handler(commands=['notificar', "notifica"])
    async def comand_user(message: types.Message):
        id = str(message.from_user.id)
        user = f"@{message.from_user.username}"
        nome = message.from_user.full_name
        tipo = message.chat.type
        chat_id = str(message.chat.id)

        if tipo == 'group' or tipo == 'supergroup':
            spam  = arq.ler_json(ca.config)['dono']['spam']

            if chat_id not in spam:

                text = (
                    f"🟢 \| Notificações ativadas\n\n"
                    f"_Certifique\-se que o bot é ADM do grupo_\n\n"
                    f"_Para desativas as notificações use o comando \/notificar_\n\n"
                )

                await message.answer(text=text, parse_mode=mark)
                spam.append(chat_id)

                arq.att_json(ca.config, spam,2,'dono', 'spam')

            else:

                text = (
                    f"❗️ \| Notificações desativadas\n\n"
                    f"_Para ativar as notificações use o comando \/notificar_\n\n"
                )

                await message.answer(text=text, parse_mode=mark)
                spam.remove(chat_id)
                arq.att_json(ca.config, spam,2,'dono', 'spam')
            
        else:
            text = (
                    f"🔴\| Não é possivel ativa as notificações aqui\n\n"
                )

            await message.answer(text=text, parse_mode=mark)

# LER MENSSAGENS DOS USUÁRIOS
@dp.message_handler()
async def funcao_ler_menssagens(message: types):
    
    id = str(message.from_user.id)
    username = f"@{message.from_user.username}"
    nome = message.from_user.full_name
    menssagem = message.text
    tipo = message.chat.type
    
    #print(message.chat.id)
    #print(message.chat.id)
    #print(message)
    
    try:
        dados = db.cliente(id)
    except:
        pass
        
    if "via_bot" in message:
        if len(menssagem.splitlines()) == 7:

            msg_split = menssagem.splitlines()

            modo = msg_split[0].split('por ')[1].upper()
            escolhida = msg_split[2].split('Opção: ')[1].upper()
            level = msg_split[4].split('Level: ')[1].upper()

            preco = msg_split[6].split('Preço: R$')[1].upper()
            
            temp = {
                "modo": modo,
                "escolhida": escolhida,
                "level": level,
                "preco": int(preco),
                "msg_id": message.message_id

            }
            
            compra_temp[id] = temp

            print(f"\n{id} | {modo} | {escolhida} | {level}")

            texto = (
                f"💳 Comprar {modo.title()}\n\n"
                f"💎 Level {level.title()}\n\n"
                f"💰 Saldo R${dados['saldo']}\n\n"
                f"💠 Preço R${preco}\n\n"
                )


    # LE O NUMERO DA CONSUL
    if menssagem.isnumeric() == True and tipo == 'private' and len(menssagem) == 12:

        if menssagem in consultaveis.keys_consul():

            cliente = db.cliente(id)

            consul = arq.ler_json(consultaveis.consul)[menssagem]
            texto = (
                f"🟢 *\| CONFIRME A SUA COMPRA*\n\n"
                f"💰 Saldo *R${cliente['saldo']}*\n\n"
                f"💠 Preço *R${consul['preco']}*\n\n"
                f"Limite *R${consul['limite']}*\n\n"
                f"Nome {r_texto.form(consul['nome']).title()}\n\n"
                f"Banco {r_texto.form(consul['consul']).title()}\n\n"
                f"Bin {consul['bin']}\n\n"
                f"⭕️ Não consulto anjo nem token\n\n"
            )

            consul_temp[id]=menssagem
            
            bt = {
                "inline_keyboard": [
                [{"text": f"{ok} Comprar", "callback_data": "comprar_consul"},
                {"text": f"{x} Cancelar", "callback_data": "apagar1"}],
                ]
            }

            threading.Thread(target=func_bot.send_bot, args=(id,texto,bt,mark,)).start()
            
            await bot.delete_message(message.chat.id, message.message_id)

        else:
            bt = {
                "inline_keyboard": [
                [{"text": f"Apagar", "callback_data": "apagar1"}],
                ]
            } 

            await message.answer(f"{x} | Esta consultável não está mais disponível", bt)     
    
    # GERA GIFT
    if menssagem.isnumeric() == True and tipo == 'private':
        if id == func_bot.id_dono or id in adm():
            
                numero = int(menssagem)
                if numero >= 1 and numero <= 2000:
                    
                    gift = gifts.salvar_gift(numero)
                    
                    bt = {
                            "inline_keyboard": [
                                
                                [{"text": f"Apagar", "callback_data": "apagar2"}],
                                
                                ]
                            }
                    
                    await message.answer(text=
                        f"[_MELHOR STORE DO 7_](https://rockcontent.com/br/wp-content/uploads/sites/2/2017/11/app-store-optimization-2.png)\n\n"
                        f"🟢 *GIFT R${gift['valor']} GERADO*\n\n"
                        f"🏷 `{gift['gift']}`\n\n"
                        f"💠 {r_texto.form(func_bot.url_store)}\n\n"
                        , reply_markup=bt, parse_mode=mark)
                    
        
    # ADICIONA MATERIAL
    if len(menssagem) >= 24 and id == func_bot.id_dono and tipo == 'private' and 'via_bot' not in message and arq.ler_json(ca.config)['dados']['adc_material'] == 'ON':
        arq.adc_txt(ca.temp_cc, f"{menssagem}\n")
            
        qtd = len(menssagem.splitlines())
            
        bt = {
                "inline_keyboard": [
                [{"text": f"Apagar", "callback_data": "apagar1"}],
                ]
                }   
            
        if qtd == 1:
                texto = f"{ok} Adicionando *{qtd}* CC"
                
        else:
                texto = f"{ok} Adicionando *{qtd}* CC's"
                
        await message.answer(texto, parse_mode=mark)     
    

    # SEND 
    if "reply_to_message" in message:
        if func_bot.id_dono == str(message["reply_to_message"]["from"]["id"]) and "/send" in menssagem and tipo== 'private':
            config = arq.ler_json(ca.config)['dados']
            

            if config['sender'] == "OFF":
                if "photo" in message["reply_to_message"]:
                    foto = message["reply_to_message"]["photo"][0]["file_id"]
                    config['photo'] = foto
                    
                # FOTO COM LEGENDA
                if "caption" in message["reply_to_message"]:
                    legenda = message["reply_to_message"]["caption"]

                    config['text'] = legenda
                    
                else:
                    # FOTO SEM LEGENDA
                    if "photo" in message["reply_to_message"]:
                        config['photo'] = foto
                        
                    else:
                        menssagem = message["reply_to_message"]
                        
                        # SÓ TEXTO
                        if "text" in menssagem:
                            menssagem = menssagem["text"]
                            config['text'] = menssagem
                            
                config['sender'] = 'ON'
                config['id'] = message.message_id +1
                arq.att_json(ca.config, config, 1, 'dados')
                return func_bot.enviar()

            else:
                await message.answer(f"🔴Aguarde até o envio anterior\n") 
            

def backup():
    
    while True:
        nome_backup = f'./backup_{func.hora_hora()}.zip'
        try:
                
            #print("CRIANDO BACKUP")
            backup_zip = zipfile.ZipFile(nome_backup, 'w')

            pasta = './'
            for diretorio, subpastas, arquivos in os.walk(pasta):
                for arquivo in arquivos:
                    nome = (os.path.join(diretorio, arquivo))
                    if 'backup' not in nome and '__pycache__' not in nome:
                        backup_zip.write(nome, compress_type=zipfile.ZIP_DEFLATED)
                    
            backup_zip.close()
            bot2.sendDocument(chat_id=arq.ler_json(ca.config)['dono']['backup'], document=open(nome_backup, 'rb'))
            os.remove(nome_backup)

            #BACKUP CLIENTES
            backup_clientes = db.clientes_json()
            nome = f'clientes_{int(time.time())}_{func_bot.user_store}.json'
            arq.salvar_json(nome, backup_clientes)
            bot2.sendDocument(chat_id=arq.ler_json(ca.config)['dono']['backup'], document=open(nome, 'rb'))
            os.remove(nome)

            #CONSUL
            bot2.sendDocument(chat_id=arq.ler_json(ca.config)['dono']['backup'], document=open(consultaveis.consul, 'rb'))


            #BACKUP CCS
            backup_ccs = db.ccs_json()
            nome2 = f'ccs_{int(time.time())}_{func_bot.user_store}.txt'

            lista = []

            for k,v in backup_ccs.items():
                lista.append(v['cc_chk'])

            lista = "\n".join(lista)

            try:
                arq.salvar_txt(nome2, lista)

                bot2.sendDocument(chat_id=arq.ler_json(ca.config)['dono']['backup'], document=open(nome2, 'rb'))

            except:
                pass

            os.remove(nome2)
            
            #print("BACKUP ENVIADO")


        except:
            pass
        
        time.sleep(600)
        
        
pedido_pendente = []

def monitora_compras_mix():
    while True:
            
        pedidos = arq.ler_json(ca.pedidos_mix)
        if len(pedidos) > 0:
            for k,v in pedidos.items():
                if k not in pedido_pendente:
                    
                    pedido_pendente.append(k)
                
                    retorno = (compras.comprar_mix(k))
                    
                    if retorno['status'] == True:
                        #remove as ccs do db
                        
                        threading.Thread(target=func_bot.edit, args=(k, v['msg_id'], f"🗳 Pacote de {v['escolhida']} mix foi enviado!",)).start()
                        
                        with open(retorno['message'], 'rb') as aqruivo:

                            bot2.sendDocument(k, aqruivo)

    
                        texto = (
                            f"🟢 Pacote de *{v['escolhida']} mix* entregue\!\n\n"
                            f"💠 Preço *R${v['preco']}*\n\n"
                            f"💰 Novo saldo *R${db.cliente(k)['saldo']}*\n\n"
                        )
                        
                        bt = {
                        "inline_keyboard": [
                            
                                [{"text": f"Menu", "callback_data": "menu"}]
                        
                            ]
                        }
                        
                        threading.Thread(target=func_bot.send_bot,args = (k, texto, bt, 'mark',)).start()
                        os.remove(retorno['message'])
                    
                    arq.del_json(ca.pedidos_mix,1,k)
                    pedido_pendente.remove(k)

                
            
        time.sleep(1)
         
def monitora_pedidos_reembolso():
    while True:
            
        pedidos = arq.ler_json(ca.pedidos_de_reembolso)
        if len(pedidos) > 0:
            for k,v in pedidos.items():
                if k not in pedido_pendente:
                    
                    pedido_pendente.append(k)
                    
                    arq.del_json(ca.pedidos_de_reembolso,1,k)

                    reembolso = compras.vereficar_reembolso(k, v['cc'], v['msg_id'])
                    
                    pedido_pendente.remove(k)

        time.sleep(1)

def monitra_reembolso():
    while True:
            
        reembolso = arq.ler_json(ca.reembolso)
        if len(reembolso) > 0:
            for k,v in reembolso.items():
                if len(v) > 0:
                    
                    for k2,v2 in v.items():
                        if v2['tempo'] + 600 <= int(time.time()):
                            arq.del_json(ca.reembolso, 2, k,k2)
                else:

                    arq.del_json(ca.reembolso, 1, k)
                    
            
        time.sleep(1)
  
def checker_pv():
    while True:
            
        pedidos = arq.ler_json(ca.pedidos_checker)
        if len(pedidos) > 0:
            
            checadas = 0                   
            aprovadas = 0                   
            reprovadas = 0                   
            erros = 0  
            for k,v in pedidos.items():
                arq.del_json(ca.pedidos_checker, 1,k)
                for c in range(0,len(v)):
                    
                    cc = v[c]
                    
                    bt = {
                            "inline_keyboard": [
                                    
                                        [{"text": f"Apagar", "callback_data": "apagar2"}]
                                
                                    ]
                                }
          
                    
                    retorno = chk.checker(cc)
                    print(retorno)
                            
                    if retorno['status'] == True:
                            if retorno['live'] == True:
                                texto = (
                                    f"{ok} \[ {c+1} \] `{cc}`\n\n{r_texto.form(retorno['message'].title())} \n\n@cosmic\store\_bot"
                                )

                                aprovadas = aprovadas +1
                                
                                func_bot.send_bot(k, texto, None, mark)
                                
                                
                            else:
                                texto = (
                                    f"{x} \[ {c+1} \] `{cc}`\n\n{r_texto.form(retorno['message'].title())} \n\n@cosmic\store\_bot"
                                )
                                
                                reprovadas = reprovadas +1
                                
                                func_bot.send_bot(k, texto, None, mark)
                                
                    else:
                        texto = (
                            f"⚠️ \[ {c+1} \] `{cc}`\n\nErro no checker\n\n@cosmic\store\_bot"
                            )
                        
                        erros = erros +1
                                
                        func_bot.send_bot(k, texto, None, mark)


                lista = []

                if aprovadas > 0:
                    lista.append(f"🟢 *{aprovadas}* Aprovadas\n\n")
                    
                if reprovadas > 0:
                    lista.append(f"🔴*{reprovadas}* Reprovadas\n\n")
                    
                if erros > 0:
                    lista.append(f"⚠️ *{erros}* Erros")

                texto  = "".join(lista)             
                    
                func_bot.send_bot(k, texto, None, mark)
                               
        time.sleep(1)

def checker_clientes():
    while True:
            
        pedidos = arq.ler_json(ca.pedidos_checker_clientes)
        if len(pedidos) > 0:
            
            
            for k,v in pedidos.items():
                arq.del_json(ca.pedidos_checker_clientes, 1, k)

                for c in range(0,len(v)):
                    cc = v[c]
                    
                    bt = {
                            "inline_keyboard": [
                                    
                                        [{"text": f"Apagar", "callback_data": "apagar2"}]
                                
                                    ]
                                }
                    
                    retorno = privado2.pre_auth(cc)

                    if retorno['status'] == True:
                            if retorno['live'] == True:
                                texto = (
                                    f"{ok} \[ {c+1} \] `{cc}`\n\n{r_texto.form(retorno['message']).title()} \n\n@cosmic\store\_bot"
                                )
                                

                                func_bot.send_bot(func_bot.id_grupo_principal, texto, None, mark)

                                arq.adc_txt("lives_grupo.txt", f"{cc}\n")
                                
                            else:
                                texto = (
                                    f"{x} \[ {c+1} \] `{cc}`\n\n{r_texto.form(retorno['message']).title()} \n\n@cosmic\store\_bot"
                                )
                                
                                
                                func_bot.send_bot(func_bot.id_grupo_principal, texto, None, mark)
                        
                    else:
                            texto = (
                                f"⚠️ \[ {c+1} \] `{cc}`\n\nErro ano checker\n\n@cosmic\store\_bot"
                            )

                            func_bot.send_bot(func_bot.id_grupo_principal, texto, None, mark)
                                
                        
                                        
        time.sleep(1)

def main():
    print("\nINICIANDO O BOT BOT\n")
    executor.start_polling(dp, skip_updates=False)
    print("\nBOT FINALIZADO\n")
    os._exit(os.X_OK)

        


threading.Thread(target=monitra_reembolso).start()

threading.Thread(target=func.atualizar_quantidade_ccs).start()

gates = 3

for c in range(1,gates):
    threading.Thread(target=monitora_compras_mix).start()

for c in range(1,gates):
    threading.Thread(target=monitora_pedidos_reembolso).start()


threading.Thread(target=api_pix.adiciona_saldo).start()
threading.Thread(target=func.adiciona_material).start()
threading.Thread(target=backup).start()
threading.Thread(target=checker_pv).start()
#threading.Thread(target=checker_clientes).start()
threading.Thread(target=func.ranking).start()


main()

