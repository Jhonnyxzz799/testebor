import sys
sys.path.insert(1, './')

from defs import ca
from defs import arq

from datetime import time
from lxml import html
import threading
import random
import json
import requests
import time

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

def checker(bin):
    bin = bin.strip()
    
    api = {}
    
    api['status'] = False
    
    if len(bin) == 6:
        if bin.isnumeric() == True:
            salvas = arq.ler_json(ca.bins)
            
            if bin in salvas:
                api = salvas[bin]
                return api
            
            else:
                retorno = puxa_bin5(bin)
                
                if retorno['status'] == False:
                    
                    
                    retorno2 = puxa_bin4(bin)
                    if retorno2['status'] == False:
                        retorno3 = puxa_bin1(bin)
                        
                        if retorno3['status'] == False:
                            api['message'] = "bin não encontrada"
                        
                        else:
                            api = retorno3
                        
                    else:
                        api = retorno2
                    
                else:
                    api = retorno
            
            if api['status'] == True:
                arq.att_json(ca.bins, api, 1, bin)
            
            return api
            
        else:
            api['message'] = 'bin inválida, digite apenas números'
            return api
        
    else:
        api['message'] = 'bin inválida, digite 6 números'
        return api


def puxa_bin1(bin):

    session = requests.Session()

    r_token = session.get('https://binlist.pro')

    token = corte(r_token.text, '<input type="hidden" name="_token" value="', '">')
    headers = {
        'authority': 'binlist.pro',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'upgrade-insecure-requests': '1',
        'origin': 'https://binlist.pro',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://binlist.pro/?',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    data = {
    '_token': token,
    'bins': bin
    }

    response = session.post('https://binlist.pro/process_bin', headers=headers, data=data)
    
    #print(response.text)
    
    retorno = corte(response.text, '<tr>', '</tr>')

    retorno = (retorno.replace('<td>','').replace('\n','').split('</td>'))
    
    api = {}
    
    busca = ['bin','bandeira','tipo','level','pais','banco']
    
    
    for c in range(0,len(busca)):
        key = busca[c]
        
        if c == 0:
            retorno_atual = retorno[c].strip()

            if retorno_atual != "" and retorno_atual != 'inicio não encontrado':
                api['status'] = True
                api[key] = retorno_atual
                
                
            else:
                api['status'] = False
                api['message'] = "bin não encontrada"

        else:
            try:
                retorno_atual = retorno[c].strip().replace(', S.A.','').replace('CREDIT','CREDITO').replace('DEBIT','DEBITO').replace('MULTIPLE','MULTIPLO')
                if 'a href=' in retorno_atual:
                    retorno_atual = corte(retorno_atual,'>','<')

                if retorno_atual == "":
                    retorno_atual = "INDEFINIDO"

                api[key] = retorno_atual
            except:
                api[key] = "INDEFINIDO"
            
            
    return api

def puxa_bin2(bin):
    

    response = requests.get(f'https://bincheck.org/{bin}')
    
    api = {}
    
    retorno = response.text

    if f'<td>{bin}</td>' in retorno:
        api['status'] = True
        
        
        bandeira = corte(corte(retorno,'<th>Brand</th>','</td>'),'">','<').strip().upper()
        tipo = corte(corte(retorno,'<th>Type</th>','</tr>'),'<td>','</td>').strip().upper().replace('CREDIT','CREDITO').replace('DEBIT','DEBITO').replace('MULTIPLE','MULTIPL')
        level = corte(corte(retorno,'<th>Category</th>','</tr>'),'<td>','</td>').strip().upper()
        banco = corte(corte(retorno,'<th class="col-md-3"> Bank</th>','</tr>'),'<td>','</td>').strip().upper()
        pais = corte(corte(retorno,'<th>Country</th>','</tr>'),'">','</a>').strip().upper().replace('BRAZIL','BRASIL')
        
        api['bin'] = bin
        api['tipo'] = tipo
        api['bandeira'] = bandeira
        api['level'] = level
        api['banco'] = banco
        api['pais'] = pais
        
        api2 = api.copy()
        
        c = 1
        for k,v in api2.items():
            if c == 1:
                pass
            
            else:
                if '--' in v or 'inicio não encontrado' in v or v=="":
                    api[k] = 'INDEFINIDO'
                    
            c = c+1

        return api
            
        
    else:
        return {
            "status":False,
            "message":'bin não encontrada',
                
                }
    
def puxa_bin3(bin):
    session = requests.Session()
    r_token = session.get('https://bincheck.io')

    token = corte(r_token.text, '<input type="hidden" name="_token" value="', '">' )
    headers = {
        'authority': 'bincheck.io',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'upgrade-insecure-requests': '1',
        'origin': 'https://bincheck.io',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://bincheck.io/?650487',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    data = {
    '_token': token,
    'bin': bin
    }

    response = session.post('https://bincheck.io/', headers=headers, data=data)
    api = {}
    
    retorno = (corte(response.text, '<form class="js-validate cardx','</form')).replace('<td style="text-align: left;">','').replace('<td width="60%" style="text-align: left;">','')
    
    if 'inicio não encontrado' not in retorno:
        api['status'] = True
        
        
        bandeira = corte(retorno, '<td width="40%">Card Brand</td>','</td>').strip()
        
        level = corte(retorno, '<td width="40%">Card Level</td>','</td>').strip()   
        tipo = corte(retorno, '<td width="40%">Card Type</td>','</td>').strip()  
        banco = corte(corte(retorno, '<td width="40%">Issuer Name / Bank</td>','</td>').strip(),'">','</a>')
        pais = corte(corte(retorno, '<td width="40%">ISO Country Name</td>','</td>').strip(),'">','</a>')
        
        api['bin'] = bin
        api['tipo'] = tipo.replace('CREDIT','CREDITO').replace('DEBIT','DEBITO').replace('MULTIPLE','MULTIPL')
        api['bandeira'] = bandeira
        api['level'] = level
        api['banco'] = banco
        api['pais'] = pais
        
        api2 = api.copy()
        
        c = 1
        for k,v in api2.items():
            if c == 1:
                pass
            
            else:
                if '------' in v or 'inicio não encontrado' in v or v=="":
                    api[k] = 'INDEFINIDO'
            c = c+1
            
        return api
            
    else:
        return {
            "status": False,
            "message": "bin não encontrada",
        }

def puxa_bin4(bin):
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'http://bins.su',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://bins.su/',
        'Accept-Language': 'pt-PT,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    data = {
    'action': 'searchbins',
    'bins': bin,
    'bank': '',
    'country': ''
    }

    api = {}

    response = requests.post('http://bins.su/', headers=headers, data=data, verify=False)

    #print(response.text)

    div = (corte(response.text, '<div id="result">', '</center>'))

    infos = corte(div, '<td>Bank</td></tr><tr>', '</tr>').replace('<td>','').split('</td>')

    if infos == "inicio não encontrado":
        return{
            "status":False,
            "message":"bin não encontrado",
        }

    try:
        api['bin'] = bin
        api['tipo'] = infos[3].replace('CREDIT','CREDITO').replace('DEBIT','DEBITO').replace('MULTIPLE','MULTIPL')
        api['bandeira'] = infos[2]
        api['level'] = infos[4]
        api['banco'] = infos[5]
        api['pais'] = infos[1]
            
        api2 = api.copy()
            
        c = 1
        for k,v in api2.items():
            if c == 1:
                pass
                
            else:
                if '------' in v or 'inicio não encontrado' in v or v=="":
                    api[k] = 'INDEFINIDO'
            c = c+1
                
        return api

    except:
        return{
            "status":False,
            "message":"Erro no bin checker",
        }
def puxa_bin5(bin):
    response = requests.get(f'http://140.82.31.167/search/bin={bin}')

    api = {}

    if "msg" in response.json():
        return{
            "status":False,
            "message":"bin não encontrado",
        }

    else:
        api = response.json()

        api['status'] = True
        api['tipo'] = api['type'].replace('CREDIT','CREDITO').replace('DEBIT','DEBITO').replace('MULTIPLE','MULTIPL')
        api['level'] = api['nivel']

        del api['type']
        del api['nivel']
        return api
