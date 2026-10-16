from def_bot import func_bot
import arq
import db
import ca
import time
import func
import r_texto
import telepot
import asyncio
import os


def dados_bot():
    return arq.ler_json(ca.config)['dados']

def dono_bot():
    return arq.ler_json(ca.config)['dono']



query = [
    'admin',
    'muda_vendas',
    'muda_pix',
    'muda_manual',
    'muda_adc_material',
    'muda_saldo_em_dobro',
    'altera_precos',
    'altera_checagem',
    'troca_gate',
    'altera_checker_atual',
    'altera_troca_atual',
    'altera_reserva_atual',
    'usuarios',
    'com_saldo',
    'estoque',
    'baixar_ccs',
    'registro_cc',
    'confirmar_reset_rate',
    'reset_rate',    
    'confirmar_reset_cc',
    'reset_cc',
    'baixar_aprovadas',
    'baixar_reprovadas',
    'baixar_registro_cc',
    'checagem',
    'relatorio_de_vendas'
]

for k,v in arq.ler_json(ca.precos).items():
    query.append(f"alteracao_preco {k.lower()}")
    query.append(f"preco_-1 {k.lower()}")
    query.append(f"preco_+1 {k.lower()}")
    query.append(f"preco_-5 {k.lower()}")
    query.append(f"preco_+5 {k.lower()}")
    
for k,v in arq.ler_json(ca.config)['checker'].items():
    if k != 'atual' and k != 'troca' and  k != 'reserva':
        query.append(f"alteracao_checker {k.lower()}")

query.append(f"alteracao_checker off")



for k,v in arq.ler_json(ca.config)['checker'].items():
    if k != 'atual' and k != 'troca' and  k != 'reserva':
        query.append(f"alteracao_troca {k.lower()}")

query.append(f"alteracao_troca off")

for k,v in arq.ler_json(ca.config)['checker'].items():
    if k != 'atual' and k != 'troca' and  k != 'reserva':
        query.append(f"alteracao_reserva {k.lower()}")

query.append(f"alteracao_reserva off")


#print(query)

ok = "🟢"
x= "🔴"
x= "🔴"
voltar = '🔙'

def comand_line(query):
    msg_upper = query.upper()
    #print(msg_upper)
    if "ADMIN" in msg_upper:
        return admin(query)    
    
    if "MUDA_VENDAS" in msg_upper:
        return muda_vendas(query)     
       
    if "MUDA_PIX" in msg_upper:
        return muda_pix(query)    

    if "MUDA_MANUAL" in msg_upper:
        return muda_manual(query)     
        
    if "MUDA_ADC_MATERIAL" in msg_upper:
        return muda_adc_material(query)         

    if "MUDA_SALDO_EM_DOBRO" in msg_upper:
        return muda_saldo_em_dobro(query)    
    
    if "ALTERA_PRECOS" in msg_upper:
        return altera_precos(query)      
      
    if "ALTERACAO_PRECO" in msg_upper:
        return alteracao_preco(query)    
          
    if "-1" in msg_upper or  "+1" in msg_upper or  "-5" in msg_upper or  "+5" in msg_upper:
        return aumenta_diminui_preco(query)    
    
    if "TROCA_GATE" in msg_upper:
        return troca_gate(query)    

    if "ALTERA_CHECKER_ATUAL" in msg_upper:
        return altera_checker_atual(query)     

    if "ALTERACAO_CHECKER" in msg_upper:
        return alteracao_checker(query)    
    
    if "ALTERA_TROCA_ATUAL" in msg_upper:
        return altera_troca_atual(query)
    
    if "ALTERACAO_TROCA" in msg_upper:
        return alteracao_troca(query)  
    
    if "ALTERA_RESERVA_ATUAL" in msg_upper:
        return altera_reserva_atual(query)
    
    if "ALTERACAO_RESERVA" in msg_upper:
        return alteracao_reserva(query)  

    if "USUARIOS" in msg_upper:
        return usuarios(query)     

    if "COM_SALDO" in msg_upper:
        return com_saldo(query)   
             
    if "ESTOQUE" in msg_upper:
        return estoque(query)    

    if "BAIXAR_CCS" in msg_upper:
        return baixar_ccs(query)
        
    if "BAIXAR_REGISTRO_CC" in msg_upper:
        return baixar_registro_cc(query)

    if "REGISTRO_CC" in msg_upper:
        return registro_cc(query) 

    if "BAIXAR_APROVADAS" in msg_upper:
        return baixar_aprovadas(query)

    if "BAIXAR_REPROVADAS" in msg_upper:
        return baixar_reprovadas(query)

        
    if "CONFIRMAR_RESET_RATE" in msg_upper:
        return confirmar_reset_rate(query)

    if "RESET_RATE" in msg_upper:
        return reset_rate(query) 
        
    if "CONFIRMAR_RESET_CC" in msg_upper:
        return confirmar_reset_cc(query)

    if "RESET_CC" in msg_upper:
        return reset_cc(query) 

    
    if "CHECAGEM" in msg_upper:
        return checagem(query) 

    
    if "RELATORIO_DE_VENDAS" in msg_upper:
        return relatorio_de_vendas(query) 

    
def bt_adm():
    dados = arq.ler_json(ca.config)
    chk = dados["checker"]["atual"].replace('_',' ').title()

    checagem = dados['dados']['checagem']
    bt_adm = {
            "inline_keyboard": [
                [{"text": f'💲 Vendas {dados_bot()["vendas_cc"]}', "callback_data": "muda_vendas"}],
                [{"text": f'❖ Pix {dados_bot()["pix"]}', "callback_data": "muda_pix"},
                {"text": f'💰 Saldo Manual {dados_bot()["manual"]}', "callback_data": "muda_manual"}],
                [{"text": f'2⃣ Saldo em dobro {dados_bot()["saldo em dobro"]}', "callback_data": "muda_saldo_em_dobro"}],
                [{"text": f'➕ Adicionar Material {dados_bot()["adc_material"]}', "callback_data": "muda_adc_material"}],
                [{"text": f'💲 Alterar Preços', "callback_data": "altera_precos"}],
                [{"text": f'🟢 Checando {checagem} até uma live', "callback_data": "checagem"}],
                [{"text": f'♻️ Gates', "callback_data": "troca_gate"}],
                [{"text": f'😃 Usuários', "callback_data": "usuarios"},
                {"text": f'😁 Com saldo', "callback_data": "com_saldo"}],
                [{"text": f'💹 Estoque', "callback_data": "estoque"},
                {"text": f'➗ Rate: {func.rate()}', "callback_data": "registro_cc"}],
                [{"text": f'💲 Relatório de vendas', "callback_data": "relatorio_de_vendas"}],
                [{"text": "♻️ Atualizar", "callback_data": "admin"},
                {"text": voltar, "callback_data": "menu"}],
                ]
            }
    
        
    
    return bt_adm


def texto_adm():

    func.dia_extrato()
    extrato = arq.ler_json(ca.extrato)
    
    dados = arq.ler_json(ca.config)
    
    texto = (
        f"🟢 Olá {r_texto.form(func_bot.dono).replace('@','')}, Seja bem vindo ao Painel adm\n\n"
        f"Pix Automático *R${extrato[func.hoje()]['entrada_pix_rs']}*\n\n"
        f"GIFT *R${extrato[func.hoje()]['entrada_gift_rs']}*\n\n"
        f"CCs vendidas hoje *{extrato[func.hoje()]['vendas']}*\n\n"
        f"Vendas hoje *R${extrato[func.hoje()]['vendas_rs']}*\n\n"
        f"Reembolsos feitos hoje *{extrato[func.hoje()]['reembolsos']}*\n\n"
        f"Valor reembolsos hoje *R${extrato[func.hoje()]['reembolsos_rs']}*\n\n"
        f"Gate de compras *{r_texto.form(dados['checker']['atual'].title())}*\n\n"
        f"Gate de trocas *{r_texto.form(dados['checker']['troca'].title())}*\n\n"
        f"Gate de reserva *{r_texto.form(dados['checker']['reserva'].title())}*\n\n"
        f"Hora *{int(time.time())}*\n\n"

    )
    
    return texto
    
def admin(query):
    dados = dados_bot()
    dono = dono_bot()
    func.dia_extrato()
    extrato = arq.ler_json(ca.extrato)
    
    return {
        "status": True,
        "alert": False,
        "message": texto_adm(),
        "bt": bt_adm(),
    }
    
def muda_vendas(query):
    dados = dados_bot()
    
    modo = dados['vendas_cc']
    
    if modo == 'OFF ⚠️':
        arq.att_json(ca.config, 'ON', 2, 'dados', 'vendas_cc')
        return admin(query)
    
    if modo == 'ON':
        arq.att_json(ca.config, 'OFF ⚠️', 2, 'dados', 'vendas_cc')
        return admin(query)  
    
def muda_pix(query):
    dados = dados_bot()
    
    modo = dados['pix']
    
    if modo == 'OFF ⚠️':
        arq.att_json(ca.config, 'ON', 2, 'dados', 'pix')
        return admin(query)
    
    if modo == 'ON':
        arq.att_json(ca.config, 'OFF ⚠️', 2, 'dados', 'pix')
        return admin(query)
    
def muda_manual(query):
    dados = dados_bot()
    
    modo = dados['manual']
    
    if modo == 'OFF ⚠️':
        arq.att_json(ca.config, 'ON', 2, 'dados', 'manual')
        return admin(query)
    
    if modo == 'ON':
        arq.att_json(ca.config, 'OFF ⚠️', 2, 'dados', 'manual')
        return admin(query)

    
def muda_adc_material(query):
    dados = dados_bot()
    
    modo = dados['adc_material']
    
    if modo == 'OFF ⚠️':
        arq.att_json(ca.config, 'ON', 2, 'dados', 'adc_material')
        return admin(query)
    
    if modo == 'ON':
        arq.att_json(ca.config, 'OFF ⚠️', 2, 'dados', 'adc_material')
        return admin(query)

    
def muda_saldo_em_dobro(query):
    dados = dados_bot()
    
    modo = dados['saldo em dobro']
    
    if modo == 'OFF ⚠️':
        arq.att_json(ca.config, 'ON', 2, 'dados', 'saldo em dobro')
        return admin(query)
    
    if modo == 'ON':
        arq.att_json(ca.config, 'OFF ⚠️', 2, 'dados', 'saldo em dobro')
        return admin(query)

def troca_gate(query):
        texto = f"_Caso escolha um checker não configurado, não irá sair live_"
        
        bt = {
                "inline_keyboard": [
                    [{"text": "🟢 Gate de compra", "callback_data": "altera_checker_atual"},
                    {"text": "⚫️ Gate de troca", "callback_data": "altera_troca_atual"}],
                    [{"text": "🔴 Gate Reserva", "callback_data": "altera_reserva_atual"}],
                    [{"text": voltar, "callback_data": "admin"}],
                    ]
                }
        
        return {
            "status": True,
            "alert": False,
            "message": texto,
            "bt": bt,
        }

#ALTERA CHECER
if True:
    def altera_checker_atual(query):
        checker = arq.ler_json(ca.config)['checker']
        
        texto = "Alteração do gate de compras"
        
        bt = {}
        
        temp = []  
        temp.append([{"text": "Desativar Checker", "callback_data": "alteracao_checker off"}])
        
        for k,v in checker.items():
            if k != "atual" and k != "troca" and k != "reserva":
                nome = k.replace('_', ' ').title()
                temp.append([{"text": f'{nome}', "callback_data": f"alteracao_checker {k.lower()}"}])
            
        
        temp.append([{"text": voltar, "callback_data": "troca_gate"}])
        
        bt['inline_keyboard'] = temp
        
        return {
            "status": True,
            "alert": False,
            "message": texto,
            "bt": bt,
        }
        
        
    def alteracao_checker(query):
        checker = query.replace('alteracao_checker ','')
        arq.att_json(ca.config, checker.lower(), 2, 'checker', 'atual')

        return {
            "status": True,
            "alert": True,
            "message": f"🟢 Checker alterado para {checker.title()}",
            "return": True
        }
   


#ALTERA GATE RESERVA
if True:
    def altera_troca_atual(query):
        checker = arq.ler_json(ca.config)['checker']
        
        texto = "Alteração do gate de trocas"
        
        bt = {}
        
        temp = []  
        temp.append([{"text": "Desativar Gate Reserva", "callback_data": "alteracao_troca off"}])
        
        for k,v in checker.items():
            if k != "atual" and k != "troca" and k != "reserva":
                nome = k.replace('_', ' ').title()
                temp.append([{"text": f'{nome}', "callback_data": f"alteracao_troca {k.lower()}"}])
            
        
        temp.append([{"text": voltar, "callback_data": "troca_gate"}])
        
        bt['inline_keyboard'] = temp
        
        return {
            "status": True,
            "alert": False,
            "message": texto,
            "bt": bt,
        }
        
        
    def alteracao_troca(query):
        checker = query.replace('alteracao_troca ','')
        arq.att_json(ca.config, checker.lower(), 2, 'checker', 'troca')

        return {
            "status": True,
            "alert": True,
            "message": f"🟢 Gate de troca alterado para {checker.title()}",
            "return": True
        }
   


#ALTERA GATE RESERVA
if True:
    def altera_reserva_atual(query):
        checker = arq.ler_json(ca.config)['checker']
        
        texto = "Alteração do gate reserva"
        
        bt = {}
        
        temp = []  
        temp.append([{"text": "Desativar Gate Reserva", "callback_data": "alteracao_reserva off"}])
        
        for k,v in checker.items():
            if k != "atual" and k != "troca" and k != "reserva":
                nome = k.replace('_', ' ').title()
                temp.append([{"text": f'{nome}', "callback_data": f"alteracao_reserva {k.lower()}"}])
            
        
        temp.append([{"text": voltar, "callback_data": "troca_gate"}])
        
        bt['inline_keyboard'] = temp
        
        return {
            "status": True,
            "alert": False,
            "message": texto,
            "bt": bt,
        }
        
        
    def alteracao_reserva(query):
        checker = query.replace('alteracao_reserva ','')
        arq.att_json(ca.config, checker.lower(), 2, 'checker', 'reserva')

        return {
            "status": True,
            "alert": True,
            "message": f"🟢 Gate reserva alterado para {checker.title()}",
            "return": True
        }
   

#ALTERA PREÇOS
if True:
        
    def altera_precos(query):
        precos = arq.ler_json(ca.precos)
        
        texto = "Alteração de preços"
        
        bt = {}
        
        temp = []  
        
        for k,v in precos.items():
            temp.append([{"text": f'{k.title()} - R${v}', "callback_data": f"alteracao_preco {k.lower()}"}])
        
        temp.append([{"text": voltar, "callback_data": "admin"}])
        
        bt['inline_keyboard'] = temp
        
        return {
            "status": True,
            "alert": False,
            "message": texto,
            "bt": bt,
        }
        
        
    def alteracao_preco(query):
        precos = arq.ler_json(ca.precos)
        
        cc = query.replace("alteracao_preco","").strip().upper()
        texto = f"Alerar preço da cc {cc.title()}"
        
        bt = {
                "inline_keyboard": [
                    [{"text": f'Preço R${precos[cc]}', "callback_data": "admin"}],
                    [{"text": f'-1', "callback_data": f"preco_-1 {cc.lower()}"},
                    {"text": f'+1', "callback_data": f"preco_+1 {cc.lower()}"}],
                    [{"text": f'-5', "callback_data": f"preco_-5 {cc.lower()}"},
                    {"text": f'+5', "callback_data": f"preco_+5 {cc.lower()}"}],
                    
                    [{"text": voltar, "callback_data": "altera_precos"}],
                    ]
                }
        
        return {
            "status": True,
            "alert": False,
            "message": texto,
            "bt": bt,
        }
        
        
    def aumenta_diminui_preco(query):
        precos = arq.ler_json(ca.precos)
                
        cc = query.split(" ")[1:]
        
        cc = " ".join(cc).upper()
        
        preco_atual = precos[cc]
        
        soma_valor = query.replace('preco_','').split(' ')[0]
        if '+' in soma_valor:
            valor = int(soma_valor.replace('+',''))
            
                
            novo_preco = preco_atual+valor
            arq.att_json(ca.precos, novo_preco,1, cc)
        else:
            valor = int(soma_valor.replace('-',''))
            novo_preco = preco_atual-valor
            arq.att_json(ca.precos, novo_preco,1, cc)

        texto = f"Alerar preço da cc {cc.title()}"
        
        bt = {
                "inline_keyboard": [
                    [{"text": f'Preço R${novo_preco}', "callback_data": "admin"}],
                    [{"text": f'-1', "callback_data": f"preco_-1 {cc.lower()}"},
                    {"text": f'+1', "callback_data": f"preco_+1 {cc.lower()}"}],
                    [{"text": f'-5', "callback_data": f"preco_-5 {cc.lower()}"},
                    {"text": f'+5', "callback_data": f"preco_+5 {cc.lower()}"}],
                    
                    [{"text": voltar, "callback_data": "altera_precos"}],
                    ]
                }
        
        return {
            "status": True,
            "alert": False,
            "message": texto,
            "bt": bt,
        }


def usuarios(query):

    clientes = db.clientes_json()
    
    usuarios = []
    
    saldo = []
    #print("usuarios")
    for k,v in clientes.items():
        if True:
            user = v['user']
            nome = v['nome']
            compras = len((v['compras'].strip()).splitlines())
            linha =  f"{k} - {user} - {nome} - SALDO: R${v['saldo']} - COMPRAS: {compras}"

            usuarios.append(linha)
            saldo.append(v['saldo'])
    
    usuarios.insert(0,f"💰 SALDO TOTAL R${sum(saldo)}")
    
    texto = "\n\n".join(usuarios)

    bt = {
            "inline_keyboard": [
                [{"text": voltar, "callback_data": "admin"}],
                ]
            }
    
    bt2 = {
            "inline_keyboard": [
                [{"text": "Apagar", "callback_data": "apagar1"}],
                ]
            }
    
    arq.salvar_txt("usuarios.txt", texto)
        
    bot = telepot.Bot(func_bot.token_bot)
    bot.sendDocument(chat_id=func_bot.id_dono, document=open("usuarios.txt", 'rb'), reply_markup=bt2)
    os.remove("usuarios.txt")

    return {
        "status": True,
        "alert": True,
        "message": "🟢 Usuários enviado",
        "return": False
    }

def com_saldo(query):

    clientes = db.clientes_json()
    
    usuarios = []
    
    saldo = []
    
    for k,v in clientes.items():
        if v['saldo'] > 0 and k != func_bot.id_dono:
            user = r_texto.form(v['user'])
            nome = r_texto.form(v['nome'])
            link = f"[{user}](tg://user?id={k})"
            linha =  f"`{k}` \- {nome} \- {link} \- *R${v['saldo']}*"

            usuarios.append(linha)
            saldo.append(v['saldo'])
    

    usuarios.insert(0,f"*💰 SALDO TOTAL R${sum(saldo)}*")
    
    texto = "\n\n".join(usuarios)

    bt = {
            "inline_keyboard": [
                [{"text": voltar, "callback_data": "admin"}],
                ]
            }
    
    bt2 = {
            "inline_keyboard": [
                [{"text": "Apagar", "callback_data": "apagar1"}],
                ]
            }
    
    if len(texto.splitlines()) > 50:
        texto = texto.replace('`','').replace('\-','-').replace("*",'').replace(") - ",' - ').replace("](tg://user?id=",' - @').replace('[','').replace('\\','')
        arq.salvar_txt(ca.cache, texto)
        bot = telepot.Bot(func_bot.token_bot)
        bot.sendDocument(chat_id=func_bot.id_dono, document=open(ca.cache, 'rb'), reply_markup=bt2)
        arq.limpar_txt(ca.cache)
        
        return {
                "status": True,
                "alert": True,
                "message": "🟢 Usuários com saldo enviado",
                "return": False
            }
    
    else:
        return {
                "status": True,
                "alert": False,
                "message": texto,
                "bt": bt,
            }


def estoque(query):
    bt = {
            "inline_keyboard": [
                [{"text": "🟢 Baixar Estoque", "callback_data": "baixar_ccs"}],
                [{"text": "🔴 Apagar Todas as CCs", "callback_data": "reset_cc"}],
                [{"text": voltar, "callback_data": "admin"}],
                ]
            }
    
    ccs = arq.ler_json(ca.quantidade)
    
    texto = []
    
    disponiveis = []
    
    for k,v in ccs.items():
        texto.append(f"`{k:<20}` \| {v}\n")
        disponiveis.append(v)
    
    texto = sorted(texto)
    
    texto.insert(0, f'*{len(ccs)} LEVEL DIFERENTE\n\n*')
    
    texto.insert(0, f'*{sum(disponiveis)} CC DISPONÍVES\n\n*')
    
    texto = "".join(texto)
    
    return {
                "status": True,
                "alert": False,
                "message": texto,
                "bt": bt,
            }
  
 
def reset_cc(query):

    bt2 = {
                "inline_keyboard": [
                    [{"text": "🟢 Apagar", "callback_data": "confirmar_reset_cc"},
                    {"text": "🔴 Cancelar", "callback_data": "estoque"}],
                    ]
                }

    
    texto = (
        "_Ao confirmar, toas as ccs do banco de dados serão apagadas_"
    )
    
    return {
                "status": True,
                "alert": False,
                "message": texto,
                "bt": bt2,
            }

 
def confirmar_reset_cc(query):
    ccs = db.ccs_json()

    db.limpa_db_cc()

    adicionadas = arq.ler_json(ca.adicionadas)['adicionadas']
    
    for k, v in ccs.items():
        if k in adicionadas:
            adicionadas.remove(k)
    
    arq.att_json(ca.adicionadas, adicionadas, 1, 'adicionadas')

    return {
                "status": True,
                "alert": True,
                "message": "🟢 Todas as ccs do banco de dados foram apagadas",
                "return": True,
            }

def baixar_ccs(query):

    bt2 = {
                "inline_keyboard": [
                    [{"text": "apagar", "callback_data": "apagar1"}],
                    ]
                }


    ccs = db.ccs_json()

    lista = []

    for k,v in ccs.items():
        lista.append(f"{v['cc_comp']}\n")

    if len(lista) > 0:
        
        arq.salvar_txt('ccs disponiveis.txt', "".join(lista))

        bot = telepot.Bot(func_bot.token_bot)
        bot.sendDocument(chat_id=func_bot.id_dono, document=open('ccs disponiveis.txt', 'rb'), reply_markup=bt2)

        os.remove('ccs disponiveis.txt')

        return {
            "status": True,
            "alert": True,
            "message": "🟢 Todas as ccs disponíveis foram enviadas",
            "return": False
        }

    else:
        return {
            "status": True,
            "alert": True,
            "message": "🔴 Não existem CCs disponíveis para baixar",
            "return": False
        }
  

def registro_cc(query):
    bt = {
            "inline_keyboard": [
                [{"text": "▼ Baixar Todas", "callback_data": "baixar_registro_cc"}],
                [{"text": "▼ Baixar Aprovadas", "callback_data": "baixar_aprovadas"},
                {"text": "▼ Baixar Reprovadas", "callback_data": "baixar_reprovadas"}],
                [{"text": f'↻ Atualizar', "callback_data": "registro_cc"}],
                [{"text": "✘ Apagar Registro", "callback_data": "reset_rate"}],
                [{"text": voltar, "callback_data": "admin"}],
                ]
            }
    
    ccs = arq.ler_txt(ca.logger_cc).strip().splitlines()
    lista = []
    lista.append(f'\n📃 O rate do seu material é *{func.rate()}*\n')
    
    for c in range(0,len(ccs)):
        lista.append(f"`{ccs[c]}`")
        if c > 8:
            break

    lista.append(f'\nHora\: {int(time.time())}\n')
    
    texto = "\n".join(lista)
    
    return {
                "status": True,
                "alert": False,
                "message": texto,
                "bt": bt,
            }

def baixar_registro_cc(query):

    bt2 = {
                "inline_keyboard": [
                    [{"text": "apagar", "callback_data": "apagar1"}],
                    ]
                }

    bot = telepot.Bot(func_bot.token_bot)
    bot.sendDocument(chat_id=func_bot.id_dono, document=open(ca.logger_cc, 'rb'), reply_markup=bt2)

    return {
                "status": True,
                "alert": True,
                "message": "🟢 Registro de ccs enviado",
                "return": False
            }

 
def baixar_aprovadas(query):

    bt2 = {
                "inline_keyboard": [
                    [{"text": "apagar", "callback_data": "apagar1"}],
                    ]
                }


    logger = arq.ler_linhas(ca.logger_cc)

    aprovadas = []
    for c in range(0,len(logger)):
        if '🟢' in logger[c]:
            aprovadas.append(logger[c])

    if len(aprovadas) > 0:
        
        arq.salvar_txt('aprovadas.txt', "".join(aprovadas))

        bot = telepot.Bot(func_bot.token_bot)
        bot.sendDocument(chat_id=func_bot.id_dono, document=open('aprovadas.txt', 'rb'), reply_markup=bt2)

        os.remove('aprovadas.txt')

        return {
            "status": True,
            "alert": True,
            "message": "🟢 Todas as ccs aprovadas foram enviadas",
            "return": False
        }

    else:
        return {
            "status": True,
            "alert": True,
            "message": "🔴 Não existem CCs aprovadas para baixar",
            "return": False
        }
  


def baixar_reprovadas(query):

    bt2 = {
                "inline_keyboard": [
                    [{"text": "apagar", "callback_data": "apagar1"}],
                    ]
                }


    logger = arq.ler_linhas(ca.logger_cc)

    reprovadas = []
    for c in range(0,len(logger)):
        if '🔴' in logger[c]:
            reprovadas.append(logger[c])

    if len(reprovadas) > 0:
        
        arq.salvar_txt('reprovadas.txt', "".join(reprovadas))

        bot = telepot.Bot(func_bot.token_bot)
        bot.sendDocument(chat_id=func_bot.id_dono, document=open('reprovadas.txt', 'rb'), reply_markup=bt2)

        os.remove('reprovadas.txt')

        return {
                "status": True,
                "alert": True,
                "message": "🟢 Todas as ccs reprovadas foram enviadas",
                "return": False
            }

    else:
        return {
            "status": True,
            "alert": True,
            "message": "🔴 Não existem CCs reprovadas para baixar",
            "return": False
        }


def reset_rate(query):

    bt2 = {
                "inline_keyboard": [
                    [{"text": "🟢 Apagar", "callback_data": "confirmar_reset_rate"},
                    {"text": "🔴 Cancelar", "callback_data": "registro_cc"}],
                    ]
                }

    
    texto = (
        "_Ao confirmar, o registro e o rate de ccs serão resetados_"
    )
    
    return {
                "status": True,
                "alert": False,
                "message": texto,
                "bt": bt2,
            }


 
def confirmar_reset_rate(query):
    arq.salvar_txt(ca.logger_cc, "REGISTRO DE CCS")
    return {
                "status": True,
                "alert": True,
                "message": "🟢 Registro e rate de ccs resetados",
                "return": True,
            }

def checagem(query):
    
    return {
                "status": True,
                "alert": True,
                "message": "⇅ Para alterar a quantidades de ccs checadas até sai uma live use o comando /checagem + o valor",
                "return": True
            }


def relatorio_de_vendas(query):
    bt2 = {
                "inline_keyboard": [
                    [{"text": f"{voltar}", "callback_data": "admin"}],
                    ]
                }

    
    extrato = arq.ler_json(ca.extrato)

    dias = []

    for k,v in extrato.items():
        dias.append(k)

    dias = dias[::-1]

    total_rs = []
    total_vendas = []

    hoje= []
    hoje_rs = []

    dias7 = []
    dias7_rs = []

    dias15 = []
    dias15_rs = []

    dias30 = []
    dias30_rs = []
    
    for c in range(0, len(dias)):
        
        total_rs.append(extrato[dias[c]]['entrada_pix_rs'])
        total_vendas.append(extrato[dias[c]]['vendas'])

        if c == 0:
            hoje_rs.append(extrato[dias[c]]['entrada_pix_rs'])
            hoje.append(extrato[dias[c]]['vendas'])

        if c+1 <= 7:
            dias7_rs.append(extrato[dias[c]]['entrada_pix_rs'])
            dias7.append(extrato[dias[c]]['vendas'])

        if c+1 <= 15:
            dias15_rs.append(extrato[dias[c]]['entrada_pix_rs'])
            dias15.append(extrato[dias[c]]['vendas'])
            
        if c+1 <= 31:
            dias30_rs.append(extrato[dias[c]]['entrada_pix_rs'])
            dias30.append(extrato[dias[c]]['vendas'])

    texto = (
        "🔵 *RELATÓRIO DE VENDAS*\n\n"

        f"     Todas as entradas *R${sum(total_rs)}*\n\n"
        f"     Todas as vendas *{sum(total_vendas)}*\n\n\n"

        f"🔵 *RELATÓRIO DE VENDAS DE HOJE*\n\n"
        f"     Entradas *R${sum(hoje_rs)}*\n\n"
        f"     Vendas *{sum(hoje)}*\n\n\n"

        f"🔵 *ÚLTIMOS 7 DIAS*\n\n"
        f"     Entradas *R${sum(dias7_rs)}*\n\n"
        f"     Vendas *{sum(dias7)}*\n\n\n"

        f"🔵 *ÚLTIMOS 15 DIAS*\n\n"
        f"     Entradas *R${sum(dias15_rs)}*\n\n"
        f"     Vendas *{sum(dias15)}*\n\n\n"

        f"🔵 *ÚLTIMOS 30 DIAS*\n\n"
        f"     Entradas *R${sum(dias30_rs)}*\n\n"
        f"     Vendas *{sum(dias30)}*\n\n\n"
        
    )
    
    return {
                "status": True,
                "alert": False,
                "message": texto,
                "bt": bt2,
            }

#estoque('query')
    
#1416422632

if __name__ == "__main__":
    print(relatorio_de_vendas("1416422632")['message'])

