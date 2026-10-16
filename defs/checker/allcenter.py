
import sys
sys.path.insert(1, '././')

from defs import arq
from defs import ca
import requests
import time

def auth():
    dados = arq.ler_json(ca.config)['checker']['allcenter pre auth']
    
    return {
        "login": dados['login'],
        "senha": dados['senha'],
        "token": dados['token'],
        "expiracao": dados['expiracao']
    }


def token():
    auth_login = auth()
    
    expiracao = int(time.time() - auth_login['expiracao'])
    
    if expiracao >= 82800:
        login = ("{\"user\":\"login\",\"pass\":\"senha\"}").replace('login',auth_login['login']).replace('senha',auth_login['senha'])
        headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "content-type": "application/json",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-requested-with": "XMLHttpRequest",
        "referrer": "https://allcenter.online/",
        "referrerPolicy": "strict-origin-when-cross-origin"}
        
        data ={
        "body": login,
        "method": "POST",
        "mode": "cors"
        }
        
        url = 'https://allcenter.online/auth'

        r = requests.post(url, headers=headers, data=data['body'])
        if r.status_code == 200:
            
            req = r.json()
            
            if req['status'] == True:
                
                arq.att_json(ca.config, int(time.time()),3, 'checker', "allcenter pre auth", 'expiracao')
                
                token = req['access_token']
                
                arq.att_json(ca.config, token, 3, 'checker', "allcenter pre auth", 'token')
                
                return token
            
    else:
        return auth_login['token']

def pre_auth(cc):
    
    try:
        url = "https://allcenter.online/DASH/api/validate"
        
        data_cc = ("{\"lista\":\"cc|mes|ano|cvv\"}").replace('cc|mes|ano|cvv', cc)
        
        headers = {
            "accept": "*/*",
            "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "authorization": f"Bearer {token()}",
            "content-type": "application/json",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-requested-with": "XMLHttpRequest",
            "referrer": "https://allcenter.online/DASH/chk/validate",
            "referrerPolicy": "strict-origin-when-cross-origin",
            "body": data_cc,
            "method": "POST",
            "mode": "cors"
        }
        
        r = requests.post(url, headers=headers, data=headers['body'])
        
        retorno = {
            "status": False,
            "live": False,
            }
        
        
        if r.status_code == 200:
            req = r.json()
            
            if req['status'] == True:
                retorno['status'] = True
                
                if req['live'] == True:
                    retorno['live'] = True
                    retorno['message'] = req['message']
                        
                else:
                    retorno['status'] = False
                    retorno['live'] = False
                    retorno['message'] = req['message']
                    
                    
                return req
            
            else:
                return {
                    "status":False,
                    "live":False,
                    "message": req['message']
                    }
            
        else:
            return {
                "status":False,
                "live":False,
                "message":"Erro ao conectar ao chk"}
            
        return {
                "status":False,
                "live":False,
                
                "message":"Sem retorno da All Center"}
        
            
    except:
            return {
                "status":False,
                "live":False,
                
                "message":"Erro no checker"}
          
 
#print(token())
#print(pre_auth('4108639646904134|04|2026|186'))