import sys
sys.path.insert(1, '././')

from defs import arq
from defs import ca
from defs import db


def form(txt):
    remover = '´\/<>()[]{}_.-|:;,+!*#='

    for c in range(0,len(remover)):
        txt = txt.replace(remover[c], f'\{remover[c]}')
        
    return txt

def repl(txt,id=None):
    dados = arq.ler_json(ca.config)
    ccs = str(len(db.ccs_json()))
    
    if id != None:
        dados_user = db.cliente(id)    
        
        try:
            nome = dados_user['nome']
            user = dados_user['user']
            saldo = dados_user['saldo']
            txt = (txt).replace('<ID_USER>', id)
            txt = (txt).replace('<NOME_USER>', f"{form(nome)}")
            txt = (txt).replace('<USER_USER>', f"{form(user)}")
            txt = (txt).replace('<SALDO_USER>', f"{saldo}")
            
        
        except:
            pass
    
    txt = (txt).replace('<CHAVE>', f"`{dados['dono']['chave_pix']}`")
    txt = (txt).replace('<BANCO>', dados['dono']['banco_da_lara'])
    txt = (txt).replace('<LARA>', dados['dono']['nome_da_lara'])
    txt = (txt).replace('<GRUPO>', f"{form(dados['dono']['user_grupo'])}")
    txt = txt.replace('<CHECKER>', form(dados['checker']['atual'].title()))
    txt = txt.replace('<SUPORTE>', form(dados['dono']['suporte']))
    txt = txt.replace('<DONO>', form(dados['dono']['dono']))
    txt = txt.replace('<CCS>', ccs)
    
    return txt

def info_start(id):
    return repl(arq.ler_txt(ca.start), id)

