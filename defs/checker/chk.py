import sys
sys.path.insert(1, '././')

import yagmail
from print_color import print

import requests
import json
import time
import random

from defs import arq
from defs import ca
from defs.checker import azkaban
from defs.checker import allcenter
from defs.checker import privado, privado2, privado3
from defs.checker import comandante
from defs.checker import thzin
from defs.checker import pagarme
from defs.checker import erede

from datetime import datetime
   
def data():
    return f"{datetime.now():%d/%m/%Y}"

def hora():
    return f"{datetime.now():%H:%M:%S}"

def logger(texto):
    log = arq.ler_linhas(ca.logger_cc)
    
    log.insert(0, texto)
    arq.salvar_linhas(ca.logger_cc, log)
    
    return texto
    
def logger_troca(texto):
    log = arq.ler_linhas(ca.logger_troca)
    
    log.insert(0, texto)
    arq.salvar_linhas(ca.logger_troca, log)
    
    return texto
     
def checker(cc):

    start = int(time.time())

    retorno = {
        "status": False,
        "live": False, 
        "message": "Checker não configurado"
    }
    
    erro = 1
    
    while retorno['status'] == False and erro < 3:
        
        checker = arq.ler_json(ca.config)['checker']['atual']
        
        if checker == 'off':
            '''rand = random.randint(1, 3)
            time.sleep(5)
            
            if rand == 1:
                retorno['live'] = True
            
            else:
                retorno['live'] = False
            '''
            retorno['status'] = True
            retorno['live'] = True
            retorno['message'] = 'CHECKER DESATIVADO'
            
            break

        if checker == 'jhon debitando':
            retorno = privado.debito(cc)
            if retorno['status'] == True:
                break      

        if checker == 'jhon debitando gate 2':
            retorno = privado2.debito(cc)
            if retorno['status'] == True:
                break   

        if checker == 'jhon debitando gate 3':
            retorno = privado3.debito(cc)
            if retorno['status'] == True:
                break  
            
        if checker == 'jhon pre auth':
            retorno = privado.pre_auth(cc)
            if retorno['status'] == True:
                break
            
        if checker == 'azkaban pre auth':
            retorno = azkaban.pre_auth(cc)
            if retorno['status'] == True:
                break 
            
        if checker == 'allcenter pre auth':
            retorno = allcenter.pre_auth(cc)
            if retorno['status'] == True:
                break    

        if checker == 'comandante pre auth':
            retorno = comandante.pre_auth(cc)
            if retorno['status'] == True:
                break

        if checker == 'thzin debitando':
            retorno = thzin.debito(cc)
            if retorno['status'] == True:
                break

        if checker == 'erede debitando':
            retorno = erede.debito(cc)
            if retorno['status'] == True:
                break

        if checker == 'pagar.me debitando':
            retorno = pagarme.debito(cc)
            if retorno['status'] == True:
                break

        
        #print(f'⚠️ {erro} ERRO | {checker.upper()} {retorno["message"]} - RETESTANDO')
        erro = erro +1
    
    end = int(time.time())

    tempo = f"{retorno['message']} - {end - start} Segundos"

    if retorno['status'] == True:
        if retorno['live'] == True:
            log = logger(f"✅ {data()} {hora()} = {cc} = {tempo}\n")
            print(log, tag='APROVADA', tag_color='green', color='white')
            
        else:
            log = logger(f"❌ {data()} {hora()} = {cc} = {tempo}\n")
            print(log, tag='REPROVADA', tag_color='red', color='white')

            
    else:
        log = logger(f"⚠️ {data()} {hora()} = {cc} = {tempo}\n")
        print(log, tag='ERRO', tag_color='yellow', color='white')
        try:
            usuario = yagmail.SMTP(user='raulpokas@gmail.com', password='helder96')
            usuario.send(to='hmlrolx89@gmail.com', subject=f"Erro no checker {checker.title()}", contents=f"Retorno: {tempo}")
        except:
            pass
        
        # CHAMAR CHECKER RESERVA (SE TIVER ATIVADO)
        if arq.ler_json(ca.config)['checker']['reserva'] != 'off':
            return reserva(cc)
            
                
    return {
        "status": retorno['status'],
        "live": retorno['live'],
        "message": retorno['message']
    }

     
def troca(cc):
    start = int(time.time())
    retorno = {
        "status": False,
        "live": False, 
        "message": "Gate de troca não configurado"
    }
    
    erro = 1
    
    while retorno['status'] == False and erro < 3:
        
        checker = arq.ler_json(ca.config)['checker']['troca']
        
        if checker == 'off':
            '''rand = random.randint(1, 3)
            time.sleep(5)
            
            if rand == 1:
                retorno['live'] = True
            
            else:
                retorno['live'] = False
            '''
            retorno['status'] = True
            retorno['live'] = True
            retorno['message'] = 'CHECKER DESATIVADO'
            
            break

        if checker == 'jhon debitando':
            retorno = privado.debito(cc)
            if retorno['status'] == True:
                break  

        if checker == 'jhon debitando gate 2':
            retorno = privado2.debito(cc)
            if retorno['status'] == True:
                break   

        if checker == 'jhon debitando gate 3':
            retorno = privado3.debito(cc)
            if retorno['status'] == True:
                break   

        if checker == 'jhon pre auth':
            retorno = privado.pre_auth(cc)
            if retorno['status'] == True:
                break
            
        if checker == 'azkaban pre auth':
            retorno = azkaban.pre_auth(cc)
            if retorno['status'] == True:
                break 
            
        if checker == 'allcenter pre auth':
            retorno = allcenter.pre_auth(cc)
            if retorno['status'] == True:
                break    

        if checker == 'comandante pre auth':
            retorno = comandante.pre_auth(cc)
            if retorno['status'] == True:
                break

        if checker == 'thzin debitando':
            retorno = thzin.debito(cc)
            if retorno['status'] == True:
                break

        if checker == 'erede debitando':
            retorno = erede.debito(cc)
            if retorno['status'] == True:
                break

        if checker == 'pagar.me debitando':
            retorno = pagarme.debito(cc)
            if retorno['status'] == True:
                break
        
        #print(f'⚠️ {erro} ERRO | {checker.upper()} {retorno["message"]} - RETESTANDO')
        erro = erro +1
    
    end = int(time.time())

    tempo = f"{retorno['message']} - {end - start} Segundos"

    if retorno['status'] == True:
        if retorno['live'] == True:
            log = logger_troca(f"✅ {data()} {hora()} = {cc} = {tempo}\n")
            print(log, tag='APROVADA', tag_color='green', color='white')
            
        else:
            log = logger_troca(f"❌ {data()} {hora()} = {cc} = {tempo}\n")
            print(log, tag='REPROVADA', tag_color='red', color='white')

            
    else:
        log = logger_troca(f"⚠️ {data()} {hora()} = {cc} = {tempo}\n")
        print(log, tag='ERRO', tag_color='yellow', color='white')
        try:
            usuario = yagmail.SMTP(user='raulpokas@gmail.com', password='helder96')
            usuario.send(to='hmlrolx89@gmail.com', subject=f"Erro no checker {checker.title()}", contents=f"Retorno: {tempo}")
        except:
            pass
                        
    # CHAMAR CHECKER RESERVA (SE TIVER ATIVADO)
    if arq.ler_json(ca.config)['checker']['reserva'] != 'off':
        return reserva(cc)

    return {
        "status": retorno['status'],
        "live": retorno['live'],
        "message": retorno['message'],
    }

def reserva(cc):
    start = int(time.time())
    retorno = {
        "status": False,
        "live": False, 
        "message": "Gate reserva não configurado"
    }
    
    erro = 1
    
    while retorno['status'] == False and erro < 3:
        
        checker = arq.ler_json(ca.config)['checker']['reserva']
        
        if checker == 'off':
            '''rand = random.randint(1, 3)
            time.sleep(5)
            
            if rand == 1:
                retorno['live'] = True
            
            else:
                retorno['live'] = False
            '''
            retorno['status'] = True
            retorno['live'] = True
            retorno['message'] = 'CHECKER DESATIVADO'
            
            break

        if checker == 'jhon debitando':
            retorno = privado.debito(cc)
            if retorno['status'] == True:
                break  

        if checker == 'jhon debitando gate 2':
            retorno = privado2.debito(cc)
            if retorno['status'] == True:
                break      
            
        if checker == 'jhon debitando gate 3':
            retorno = privado3.debito(cc)
            if retorno['status'] == True:
                break  

        if checker == 'jhon pre auth':
            retorno = privado.pre_auth(cc)
            if retorno['status'] == True:
                break
            
        if checker == 'azkaban pre auth':
            retorno = azkaban.pre_auth(cc)
            if retorno['status'] == True:
                break 
            
        if checker == 'allcenter pre auth':
            retorno = allcenter.pre_auth(cc)
            if retorno['status'] == True:
                break    

        if checker == 'comandante pre auth':
            retorno = comandante.pre_auth(cc)
            if retorno['status'] == True:
                break

        if checker == 'thzin debitando':
            retorno = thzin.debito(cc)
            if retorno['status'] == True:
                break

        if checker == 'erede debitando':
            retorno = erede.debito(cc)
            if retorno['status'] == True:
                break

        if checker == 'pagar.me debitando':
            retorno = pagarme.debito(cc)
            if retorno['status'] == True:
                break


        #print(f'⚠️ {erro} ERRO | {checker.upper()} {retorno["message"]} - RETESTANDO')
        erro = erro +1
    
    end = int(time.time())

    tempo = f"{retorno['message']} - {end - start} Segundos"

    if retorno['status'] == True:
        if retorno['live'] == True:
            log = logger(f"✅ {data()} {hora()} = {cc} = {tempo}\n")
            print(log, tag='APROVADA', tag_color='green', color='white')
            
        else:
            log = logger(f"❌ {data()} {hora()} = {cc} = {tempo}\n")
            print(log, tag='REPROVADA', tag_color='red', color='white')

            
    else:
        log = logger(f"⚠️ {data()} {hora()} = {cc} = {tempo}\n")
        print(log, tag='ERRO', tag_color='yellow', color='white')
        try:
            usuario = yagmail.SMTP(user='raulpokas@gmail.com', password='helder96')
            usuario.send(to='hmlrolx89@gmail.com', subject=f"Erro no checker {checker.title()}", contents=f"Retorno: {tempo}")
        except:
            pass
                
    return {
        "status": retorno['status'],
        "live": retorno['live'],
        "message": retorno['message'],
    }


#print(chk_cosmics('4108639646904134|04|2026|186'))
#print(chk_allcenter('4108639646904134|04|2026|186'))