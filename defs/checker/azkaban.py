import sys
sys.path.insert(1, '././')

from defs import arq
from defs import ca
import requests

def auth():
    dados = arq.ler_json(ca.config)['checker']['azkaban pre auth']
    
        
    return {
        "login": dados['login'],
        "senha": dados['senha'],
        "token": dados['token']
    }

def pre_auth(cc):
    
    login = auth()
    try:
            url = f"https://zeoncentr1122&op/oAuth&listakers/0auth/?usuario=kaue&senha=1122&ZeroAuth&lista"

            r = requests.get(url)

            req = r.json()

            
            if "error" in req:
                    retorno = {
                    "status": False,
                    "live": False,
                    "message": req['retorno']
                    }
                
                    return retorno

            
            else:
                
                if req['success'] == True:
                    retorno = {
                        "status": True,
                        "live": True,
                        "message": req['retorno']
                    }
                    
                    return retorno
                
                
                else:
                    if req['success'] == False:
                        retorno = {
                        "status": True,
                        "live": False,
                        "message": req['retorno']
                        }
                    
                        return retorno
            
                retorno = {
                    "status": False,
                    "live": False,
                    "message": "Sem retorno do RtChk"
                    }
                    
                return retorno
            
    except:
        
        retorno = {
            "status": False,
            "live": False,
            "message": "Erro ao se conectar ao chk"
            }
        
        return retorno
    
def debito(cc):
    
    login = auth()
    
    try:
        
            url = f"https://zeoncentral.shop/oAuth&listakers/0auth/?usuario=kaue&senha=1122&ZeroAuth&lista"

            r = requests.get(url)
            req = r.json()
            
            if "error" in req:
                    retorno = {
                    "status": False,
                    "live": False,
                    "message": req['retorno']
                    }
                
                    return retorno
            
            else:
                
                if req['success'] == True:
                    retorno = {
                        "status": True,
                        "live": True,
                        "message": req['retorno']
                    }
                    
                    return retorno
                
                
                else:
                    if req['success'] == False:
                        retorno = {
                        "status": True,
                        "live": False,
                        "message": req['retorno']
                        }
                    
                        return retorno
            
                retorno = {
                    "status": False,
                    "live": False,
                    "message": "Sem retorno do azkaban"
                    }
                    
                return retorno
            
    except:
        
        retorno = {
            "status": False,
            "live": False,
            "message": "Erro ao se conectar ao chk"
            }
        
        return retorno


#print(pre_auth('4108633971898938|07|2028|784'))