import sys
sys.path.insert(1, '././')

from defs import db, func, arq, ca, r_texto, separador
from defs.def_bot import func_bot
import time
from defs.checker import chk
import threading

comandos = [
    'attfoto',
    'attstart',
    'attsaldo',
    'ban',
    'unban',
    'garantias',
    'info',
    'checagem',
]

ok = "✅"
x= "❌"

def comand_line(menssagem):
    msg_upper = menssagem.upper()
    if "ATTFOTO" in msg_upper:
        return attfoto(menssagem)
    
    if "ATTSTART" in msg_upper:
        return attstart(menssagem)

    if "ATTSALDO" in msg_upper:
        return attsaldo(menssagem)
    
    if "UNBAN" in msg_upper:
        return unban(menssagem)  
      
    if "BAN" in msg_upper:
        return ban(menssagem)   
     
    if "GARANTIAS" in msg_upper:
        return garantias(menssagem)  
          
    if "INFO" in msg_upper:
        return info(menssagem)       

    if "CHECAGEM" in msg_upper:
        return checagem(menssagem)     
              
def replace_comando(menssagem):
    for c in range(0, len(comandos)):
        return " ".join(menssagem.split(' ')[1:])


def attfoto(menssagem):
    url = replace_comando(menssagem)
    
    arq.att_json(ca.config, url, 2, 'dados', 'foto')
    
    return {
        "status": True,
        "message": f"{ok} Foto Principal atualizada"
    }
    

def attstart(menssagem):
    texto = replace_comando(menssagem)
    
    
    if len(texto.strip()) < 1:
        arq.salvar_txt(ca.start, texto)
        return {
        "status": False,
        "message": f"{x} Texto de início não pode ser vazio"
    }
    
    return {
        "status": True,
        "message": f"{ok} Texto de início alterado"
    }
    

def attsaldo(menssagem):
    msg = replace_comando(menssagem)
    
    try:
        id = msg.split(' ')[0]
        novo_saldo = int(msg.split(' ')[1])
        
    except:
        return {
        "status": False,
        "message": r_texto.form(f"Digite ID | Novo saldo\n\nEx: `/attsaldo {func_bot.id_dono} 50`")
    }
    
    cliente = db.cliente(id)

    if cliente != False:
        saldo_antigo = cliente['saldo']
        cliente['saldo'] = novo_saldo
        
        threading.Thread(target=db.atualiza_cadastro, args=(cliente,)).start()
        
        return {
                "status": True,
                "message": f"{ok} {r_texto.form(cliente['nome'])} \- [{r_texto.form(cliente['user'])}](tg://user?id={id})\n\nSaldo antigo R${saldo_antigo}  \-  *Novo saldo R${novo_saldo}*"
            }
    else:
        
        return {
            "status": False,
            "message": r_texto.form(f"{x} ID {id} Não encontrado")
        }
  
      
def ban(menssagem):
    msg = replace_comando(menssagem)
            
    try:
        id = msg.split(' ')[0]
        id = int(id)
        id = str(id)
        cliente = db.cliente(id)

        if cliente != False:
            if cliente['autorizacao'] == True:
                
                cliente['autorizacao'] = 0
                cliente['ban'] = 4
                
                threading.Thread(target=db.atualiza_cadastro, args=(cliente,)).start()
                
                return {
                    "status": True,
                    "message": f"{ok} [{r_texto.form(cliente['nome'])}](tg://user?id={id}) Banido"
                }
                
            else:
                return {
                "status": False,
                "message": f"⚠️ [{r_texto.form(cliente['nome'])}](tg://user?id={id}) Já está banido"
                }
            
        else:
            return {
            "status": False,
            "message": f"{x} ID não encontrado"
            }
    except:
        return {
        "status": False,
        "message": r_texto.form(f"Digite o ID\n\nEx: `/ban {func_bot.id_dono}`")
    }
      
def unban(menssagem):
    msg = replace_comando(menssagem)
    
        
    try:
        id = msg.split(' ')[0]
        id = int(id)
        id = str(id)
        cliente = db.cliente(id)

        if cliente != False:
            
            if cliente['autorizacao'] == False:
                            
                cliente['autorizacao'] = 1
                cliente['ban'] = 0

                threading.Thread(target=db.atualiza_cadastro,args=(cliente,)).start()
                
                return {
                    "status": True,
                    "message": f"{ok} [{r_texto.form(cliente['nome'])}](tg://user?id={id}) Desbanido"
                }
                
            else:
                return {
                "status": False,
                "message": f"⚠️ [{r_texto.form(cliente['nome'])}](tg://user?id={id}) Não está banido"
                }
            
        else:
            return {
            "status": False,
            "message": f"{x} ID não encontrado"
            }
    except:
        return {
        "status": False,
        "message": r_texto.form(f"Digite o ID\n\nEx: `/unban {func_bot.id_dono}`")
    }
      

def garantias(menssagem):
    msg = replace_comando(menssagem)
    
    arq.salvar_txt(ca.garantias, msg)
    
    return {
        "status": True,
        "message": f"{ok} Garantias atualizadas"
    }

def info(menssagem):
    msg = replace_comando(menssagem)
    id = msg
    
    try:
        id = msg
        cliente = db.cliente(id)

        if cliente != False:
            
            link = f"[{r_texto.form(cliente['user'])}](tg://user?id={id})"
            compras = []
            
            comp = cliente['compras'].strip().splitlines()
            
            for c in range(0, 3):
                try:
                    compras.append(f'`{comp[c]}`')
                except:
                    pass
                
            compras = "\n".join(compras)
            texto = (
                f"ID `{id}`\n\n"
                f"Nome `{r_texto.form(cliente['nome'])}`\n\n"
                f"User {link}\n\n"
                f"Saldo *R${cliente['saldo']}*\n\n"
                f"Gifts Resgatados *{len(cliente['gifts'].strip().splitlines())}*\n\n"
                f"Compras *{len(cliente['compras'].strip().splitlines())}*\n\n"
                f"{compras}"
            )
            
            return {
                "status": False,
                "message": texto
                }
            
        else:
            return {
            "status": False,
            "message": f"{x} ID não encontrado"
            }
    except:
        return {
        "status": False,
        "message": r_texto.form(f"Digite o ID\n\nEx: `/info {func_bot.id_dono}`")
    }


def checagem(menssagem):
    msg = replace_comando(menssagem)
    
    if msg.isnumeric():
        msg = int(msg)
        if msg > 0 and msg <= 20:

            arq.att_json(ca.config, msg, 2, 'dados', "checagem")

            return {
                "status": True,
                "message": f"{ok} Agora o bot vai checar {msg} CC até retorna algo para o usuário"
            }


        else:
                
            return {
                "status": False,
                "message": f"{x} Valor inválido, escolha um valor entre 1 e 20"
            }

    else:
        return {
            "status": False,
            "message": f"{x} Para alterar a quantidades de ccs checadas até sai uma live use o comando \/checagem \+ o valor"
        }


#print(info('info 1416422632'))

#print(send('send tste'))
#1416422632