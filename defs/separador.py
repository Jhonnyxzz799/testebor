import re
import sys
sys.path.insert(1, '././')
from defs import arq
from datetime import datetime
from defs import bin
from defs import ca

c_remove = '''[
    ]
    "
    '
    :
    !
    @
    #
    »
    >
    =
    $
    ✓
    titular
    -sem numero
    -sem telefone
    sem telefone
    sem numero
    sem cpf
    pegar cpfa fatura
    pegar cpf fatura
    pegar cpf na fatura
    pega cpf fatura
    PEGAR NA FATURA 
    pega cpf na fatura
    Numero do Cartão
    numero do cartão
    numero do cartao
    número do cartão
    número do cartao
    do cartao
    do cartão
    cartao
    cartão
    número
    numero
    número do
    numero do
    XXXX
    SEM 
    COM
    SALDO
    R$
    NOME
    CC
    SENHA
    DATA
    CVV
    CPF
    celular
    CELL
    CEL
    TELEFONE
    senha
    validade
    data
    cpf
    nome
    celular
    telefone
    limite
    Atual
    Total
    Dia Venc
    OBS
    ITAUCARD
    click
    Exclusive
    Gold
    mc
    Credicard
    hipercard
    classico
    classic
    platinum
    inter
    passai
    sams
    Azul
    Pass
    multiplo
    Uniclass
    zero
    Internacional
    INTERNATIONAL
    IPIRANGA
    pref
    Nacional
    Mult
    latam
    PONTO FRIO
    MARISA
    EXTRA
    ITAU
    AVISO
    card
    uni
    PLAT
    LUIZA OURO
    tel
    preferencial
    mbank
    ou
    EMPRESTIMO
    ENDEREÇO
    AVENIDA
    COMPLEMENTO
    EMAIL
    INFORMAÇÕES
    PAIS
    BRAZIL
    BR
    BANCO
    CREDIT
    MENSAGEM
    PAGAMENTO
    APROVADO
    REPROVADO
    COPYRIGHT
    AZKABANCENTER
    NÍVEL
    TIPO
    BANDEIRA
    MASTER
    UNIBANCO
    SA
    POTUE
    POTUE**
    **
    *'''

def search_cc(texto):
    texto = texto.replace('|', ' | ').replace('<', ' | ').replace('>', ' | ').replace('  ', ' ').replace('[', ' ').replace(']', ' ').upper()
    texto = f" {texto} "
    cc = '❌'
    r = re.compile(r".\d{16}")
    for match in r.finditer(texto):
        cc = (match.group()).strip()
        cc = f"{cc[:4]} {cc[4:8]} {cc[8:12]} {cc[12:]}"
        
    if cc == '❌':
                
        r = re.compile(r".\d{3} .\d{3} .\d{3} .\d{3}")
        for match in r.finditer(texto):
            cc = (match.group()).strip()      
    
    return cc
   
def search_senha(texto):
    texto = texto.replace('|', ' | ').replace('  ', ' ').replace('	', ' ').upper()
    texto = f" {texto} "
    senha = '❌'
    cc = search_cc(texto)
    cpf = search_cpf(texto)
    telefone = search_telefone(texto)
    nome = search_nome(texto)
    validade = search_validade(texto)
    
    texto = str(texto.replace(cc, '').replace(cc.replace(' ',''), '').replace(validade, '').replace(cpf, '').replace(telefone, '').replace(nome, ''))
    r = re.compile(r" \d{4} ")
    for match in r.finditer(texto):
        senha = (match.group()).strip()

    if senha == '❌':
        r = re.compile(r" \d{6} ")
        for match in r.finditer(texto):
            senha = (match.group()).strip()

    return senha    
            
def search_validade(texto):
    texto = texto.replace('  ', ' ').replace('»', '/').replace('[', ' ').replace(']', ' ').replace(' / ', '/').upper()
    texto = f" {texto} "
        
    validade = '❌'
    
    mudança = {
        "jan/": " 01/",
        "fev/": " 02/",
        "mar/": " 03/",
        "abr/": " 04/",
        "mai/": " 05/",
        "jun/": " 06/",
        "jul/": " 07/",
        "ago/": " 08/",
        "set/": " 09/",
        "out/": " 10/",
        "nov/": " 11/",
        "dez/": " 12/",

        "/22": "/2022|",
        "/23": "/2023|",
        "/24": "/2024|",
        "/25": "/2025|",
        "/26": "/2026|",
        "/27": "/2027|",
        "/28": "/2028|",
        "/29": "/2029|",
        "/30": "/2030|",
                
        "|22|": "/2022|",
        "|23|": "/2023|",
        "|24|": "/2024|",
        "|25|": "/2025|",
        "|26|": "/2026|",
        "|27|": "/2027|",
        "|28|": "/2028|",
        "|29|": "/2029|",
        "|30|": "/2030|",
                                        
        "|2022": "/2022|",
        "|2023": "/2023|",
        "|2024": "/2024|",
        "|2025": "/2025|",
        "|2026": "/2026|",
        "|2027": "/2027|",
        "|2028": "/2028|",
        "|2029": "/2029|",
        "|2030": "/2030|",
                
        "|": " | ",
        "  ": " "
        }
            
            
    for k,v in mudança.items():
        texto = texto.replace(k,v)

                    
    r = re.compile(r".\d{1}/.\d{3}")
    for match in r.finditer(texto):
        validade = (match.group()).strip()
        
    if validade != '❌':
        mes = validade.split('/')[0]
        ano = validade.split('/')[1]
        if mes.isnumeric() and ano.isnumeric():    
            if int(ano) > 2020 and int(ano) < 2031:
                if int(mes) > 0 and int(mes) < 13:
                    if int(ano) == datetime.now().year and int(mes) < datetime.now().month:
                        return '❌'
                        
                else:
                    return '❌'
            else:
                return '❌'
        else:
            return '❌'
    
    else:
        return '❌'
    
    return validade

def search_cvv(texto):
    texto = texto.replace('|', ' | ').replace('  ', ' ').replace('<', ' ').replace('>', ' ').replace('	', ' ').replace('»', ' ').replace('[', ' ').replace(']', ' ').upper()
    texto = f" {texto} "
    cvv = '❌'
    
    cc = search_cc(texto)
    senha = search_senha(texto)
    cpf = search_cpf(texto)
    telefone = search_telefone(texto)
    nome = search_nome(texto)
    validade = search_validade(texto)
    
    texto = str(texto.replace(cc, '').replace(cc.replace(' ',''), '').replace(validade, '').replace(cpf, '').replace(telefone, '').replace(nome, '').replace(senha, ''))
    
    
    r = re.compile(r" .\d{2} ")
    for match in r.finditer(texto):
        cvv = (match.group()).strip()

    return cvv
    
def search_cpf(texto):
    texto = texto.replace('|', ' | ').replace('  ', ' ').upper()
    texto = f" {texto} "
        
    cpf = '❌'
    
    r = re.compile(r".\d{2}..\d{2}..\d{2}-.\d{1}")
    for match in r.finditer(texto):
        cpf = (match.group()).strip()
        
    if cpf == '❌':
                
        r = re.compile(r".\d{2}..\d{2}..\d{2}-.\d{0}")
        for match in r.finditer(texto):
            cpf = (match.group()).strip()      

    if cpf == '❌':
        r = re.compile(r" .\d{10} ")
        for match in r.finditer(texto):
            cpf = (match.group()).strip()
            cpf = f"{cpf[0:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    
    if '.' in cpf and '-' in cpf:
        return cpf    


    else:
        return '❌'
    
def search_telefone(texto):
    texto = texto.replace('|', ' | ').replace('  ', ' ').replace('  ', ' ').upper()
    texto = f" {texto} "
    telefone = '❌'

    # 9
    if True:
        if telefone == '❌':
            r = re.compile(r"(.\d{2}).\d{0} .\d{4}-\d{4}")
            for match in r.finditer(texto):
                telefone = (match.group()).strip()

        if telefone == '❌':
            r = re.compile(r"(.\d{2}).\d{5}-\d{4}")
            for match in r.finditer(texto):
                telefone = (match.group()).strip()
                telefone = f'{telefone[0:4]} 9{telefone[5:]}'
        
        if telefone == '❌':
            r = re.compile(r"(.\d{2}).\d{0} .\d{8}")
            for match in r.finditer(texto):
                telefone = (match.group()).strip()
                telefone = f'{telefone[0:4]} {telefone[5:10]}-{telefone[10:]}'
        
        if telefone == '❌':
            r = re.compile(r"(.\d{2}).\d{9}")
            for match in r.finditer(texto):
                telefone = (match.group()).strip()
                telefone = f'{telefone[0:4]} {telefone[4:9]}-{telefone[9:]}'
    # 8 
    if True:
        if telefone == '❌':
            r = re.compile(r"(.\d{2}).\d{0} .\d{3}-\d{4}")
            for match in r.finditer(texto):
                telefone = (match.group()).strip()

        if telefone == '❌':
            r = re.compile(r"(.\d{2}).\d{4}-\d{4}")
            for match in r.finditer(texto):
                telefone = (match.group()).strip()
                telefone = f'{telefone[0:4]} {telefone[4:]}'
        
        if telefone == '❌':
            r = re.compile(r"(.\d{2}).\d{0} .\d{8}")
            for match in r.finditer(texto):
                telefone = (match.group()).strip()
                telefone = f'{telefone[0:4]} {telefone[5:9]}-{telefone[9:]}'
        
        if telefone == '❌':
            r = re.compile(r"(.\d{2}).\d{8}")
            for match in r.finditer(texto):
                telefone = (match.group()).strip()
                telefone = f'{telefone[0:4]} {telefone[4:8]}-{telefone[8:]}'

    return telefone    

def search_nome(texto):
    texto = texto.replace('|', ' | ').replace('  ', ' ').upper()
    texto = f" {texto} "
    
    nome = texto
    
    # TRATANDO NOME
    remover = '"0123456789().-/|❌][{}:;,\n'
    
    for c in range(0,len(remover)):
        
        for c2 in range(0,len(texto)):
            if remover[c] == texto[c2]:
                nome = nome.replace(remover[c],'').replace('\n','').upper().strip()
    
    remover_mais = c_remove.splitlines()
            
    for c in range(0, len(remover_mais)):
        remover2 = remover_mais[c].strip().replace('\n','').upper().strip()
        remover2 = f"{remover2} "
        
        nome = nome.replace(remover2,'').replace('\n','').upper().strip()
        nome = f"{nome} "
        
    
    if len(nome) < 3:
        
        nome = '❌'
    else:
        if nome.strip()[0] == 'H':
            nome = nome.replace(nome.strip()[0],"").strip()
        
    return nome    

def remover_duplicatas(texto):
    
    temp = []
    qtd = len(texto)
    linhas = texto.strip().splitlines()
    dados = {}
    
    for c in range(0, qtd):
        
        linha_atual = f'{linhas[c]} '
        
        if linha_atual != None:
            if len(linha_atual) >= 23:
                dados[linha_atual] = f"{linha_atual.strip()}\n"
        
        else:
            continue
    
    for k,v in dados.items():
        temp.append(v)
        
    return "".join(temp)

def separar_cc(linha):
    linha = f" {linha} "
    cc = search_cc(linha)
    cc = cc.replace(' ','')
    linha = linha.replace(cc,'')
    validade = search_validade(linha)
    validade = validade.replace('/','|')
    
    linha = linha.replace(validade,'')
    
    cvv = search_cvv(linha)
    linha = linha.replace(cvv,'')
    
    if cc == '❌' or validade == '❌' or cvv == '❌':
        return 
    
    else:
        cc_sep = (f"{cc}|{validade}|{cvv}")
            
        return cc_sep       

def separar_consul(linha):
    
    cc = search_cc(linha)
    linha = linha.replace(cc,'')

    validade = search_validade(linha)
    linha = linha.replace(validade,'')
    
    cpf = search_cpf(linha)
    linha = linha.replace(cpf,'')
    
    telefone = search_telefone(linha)
    linha = linha.replace(telefone,'')
        
    senha = search_senha(linha)
    linha = linha.replace(senha,'')
    
    cvv = search_cvv(linha)
    linha = linha.replace(cvv,'')
    
    nome = search_nome(linha)
    
    if cc == '❌':
        return
    
    if len(linha) >= 16:
                 
        consultavel = (f"00 | 00 | --- | --- | {cc} | {senha} | {validade} | {cvv} | {cpf} | {telefone} | {nome}")
            
        return consultavel       

    else:
        return

def separar_linhas(txt, modo = 'cc', envio='normal'):
    
    temp = []
    
    msg = remover_duplicatas(txt).splitlines()
    qtd = len(msg)
    bins = arq.ler_json(ca.bins)
    if modo == 'cc':
        for c in range(0, qtd):
            linha_atual = msg[c]
            cc_atual = separar_cc(linha_atual)
            bincc = cc_atual[:6]
            
            if cc_atual != None:
                
                if envio == 'normal':
                    temp.append(f"{cc_atual}\n")       
                
                if envio == 'arquivo':
                    bin_atual = bin.checker(bincc)
                    
                    if bin_atual['status'] == 'ok':
                        info_bin = f"{bin_atual['bandeira']}|{bin_atual['tipo']}|{bin_atual['level']}|{bin_atual['banco']}|{bin_atual['pais']}"
                        temp.append(f"{cc_atual}|{info_bin}\n\n")
                    
                    else:
                        info_bin = f"INDEFINIDO|INDEFINIDO|INDEFINIDO|INDEFINIDO|INDEFINIDO"
                        temp.append(f"{cc_atual}|{info_bin}\n\n")
            else:
                pass
        
        separadas = "".join(temp)
        
        if envio == 'normal':
            return separadas   
             
        if envio == 'arquivo':
            return separadas
    
    if modo == 'consul':
        
        temp = []
        
        for c in range(0, qtd):
            linha_atual = msg[c]
            consul = separar_consul(linha_atual)
            if consul != None:
                consul = consul.replace("00 | 00 | --- | --- | ",'')
                bin_consul = consul.replace(' ','')[:6]
                
                bin_consul = bin.checker(bin_consul) 
                if bin_consul['status'] == 'ok':
                    bin_consul = bin_consul['banco']
                    
                else:
                    bin_consul = 'INDEFINIDO'
                
                if envio == 'normal':
                    temp.append(f"{bin_consul} | {consul}\n")
                             
                if envio == 'arquivo':
                    temp.append(f"{bin_consul}\n00 | 00 | --- | --- | {consul}\n\n")
                        
        separadas = "".join(temp)
        if envio == 'arquivo':
            separadas.replace('`', '')
            
        return(separadas)


# IDENTIFICADOR DE CONSUL

def sep_auto_consul(msg, envio='normal'):
    
    qtd_char = len(msg)
    
    msg = msg.splitlines()
    qtd = len(msg)
    
    temp = {}
    
    if envio == 'normal':
        
        if qtd_char > 30:
            
            for c in range(0, qtd):
                try:

                    cc = search_cc(msg[c])
                    senha = search_senha(msg[c])
                    validade = search_validade(msg[c])
                    cvv = search_cvv(msg[c])
                    cpf = search_cpf(msg[c])
                    if '(' in msg[c] and ')' in msg[c] and len(msg[c]) > 8:
                        
                        telefone = search_telefone(msg[c])
                        
                    else:
                        telefone = '❌'
                        
                    nome = search_nome(msg[c])

                    if cc != '❌':
                        print(f"{c+1}/{qtd} - {cc}")

                        temp[cc] = {
                            "cc": cc,
                            "senha": '',
                            "validade": '',
                            "cvv": '',
                            "cpf": '',
                            "telefone": '',
                            "nome": '',
                            "banco": ''
                        }
                        ultima_cc = cc
                        
                        bin_cc = cc.replace(" ", "")[:6]
                        
                        bin_atual = bin.checker(bin_cc)
                    
                        if bin_atual['status'] == 'ok':
                            temp[cc]['banco'] = f"{bin_atual['banco']}"
                            
                        else:
                            temp[cc]['banco'] = 'INDEFINIDO'
                        
                    
                    if senha != '❌':
                        if temp[ultima_cc]['senha'] == '':
                            temp[ultima_cc]['senha'] = senha
                            
                    if validade != '❌':
                        if temp[ultima_cc]['validade'] == '':
                            temp[ultima_cc]['validade'] = validade          
                        
                    if cvv != '❌':
                        if temp[ultima_cc]['cvv'] == '' and senha not in ultima_cc:
                            temp[ultima_cc]['cvv'] = cvv

                    if cpf != '❌':
                        if temp[ultima_cc]['cpf'] == '':
                            temp[ultima_cc]['cpf'] = cpf          
                        
                    if telefone != '❌':
                        if temp[ultima_cc]['telefone'] == '':
                            temp[ultima_cc]['telefone'] = telefone               
                        
                    if nome != '❌':
                        if temp[ultima_cc]['nome'] == '':
                            
                            temp[ultima_cc]['nome'] = nome
                except:
                    pass

            lista = []
            for k,v in temp.items():
                
                senha = v['senha']
                if senha == '':
                    senha = '❌'
                    
                validade = v['validade']
                if validade == '':
                    validade = '❌'
                        
                cvv = v['cvv']
                if cvv == '':
                    cvv = '❌'
                        
                cpf = v['cpf']
                if cpf == '':
                    cpf = '❌'        
                
                telefone = v['telefone']
                if telefone == '':
                    telefone = '❌'        
                
                nome = v['nome']
                if nome == '':
                    nome = '❌'
                        
                        
                lista.append(f"{k} | {senha} | {validade} | {cvv} | {cpf} | {telefone} | {nome} | {temp[k]['banco']}\n")
            
            if len(lista) < 1:
                return {
                "status": False,
                "message": "❌ Nenhuma consultável identificada"
            }
            
            else:
                arq.salvar_linhas(ca.cache, lista)
                
                retorno = arq.ler_txt(ca.cache)
                
                arq.limpar_txt(ca.cache)
                
                return {
                    "status": True,
                    "message": retorno
                }
        
        else:
            return {
                "status": False,
                "message": "❌ Nenhuma consultável identificada"
            }


    else:
        if qtd_char > 30:
            
            for c in range(0, qtd):
                try:
                    cc = search_cc(msg[c])
                    senha = search_senha(msg[c])
                    validade = search_validade(msg[c])
                    cvv = search_cvv(msg[c])
                    cpf = search_cpf(msg[c])
                    if '(' in msg[c] and ')' in msg[c] and len(msg[c]) > 8:
                        
                        telefone = search_telefone(msg[c])
                        
                    else:
                        telefone = '❌'
                        
                    nome = search_nome(msg[c])

                    if cc != '❌':
                        temp[cc] = {
                            "cc": cc,
                            "senha": '',
                            "validade": '',
                            "cvv": '',
                            "cpf": '',
                            "telefone": '',
                            "nome": '',
                            "banco": ''
                        }
                        
                        ultima_cc = cc
                        
                        bin_cc = cc.replace(" ", "")[:6]
                        
                        bin_atual = bin.checker(bin_cc)
                    
                        if bin_atual['status'] == 'ok':
                            temp[cc]['banco'] = f"{bin_atual['banco']}"
                            
                        else:
                            temp[cc]['banco'] = 'INDEFINIDO'
                    
                    if senha != '❌':
                        if temp[ultima_cc]['senha'] == '':
                            temp[ultima_cc]['senha'] = senha
                            
                    if validade != '❌':
                        if temp[ultima_cc]['validade'] == '':
                            temp[ultima_cc]['validade'] = validade          
                        
                    if cvv != '❌':
                        if temp[ultima_cc]['cvv'] == '' and senha not in ultima_cc:
                            temp[ultima_cc]['cvv'] = cvv

                    if cpf != '❌':
                        if temp[ultima_cc]['cpf'] == '':
                            temp[ultima_cc]['cpf'] = cpf          
                        
                    if telefone != '❌':
                        if temp[ultima_cc]['telefone'] == '':
                            temp[ultima_cc]['telefone'] = telefone               
                        
                    if nome != '❌':
                        if temp[ultima_cc]['nome'] == '':
                            
                            temp[ultima_cc]['nome'] = nome
                except:
                    pass

            lista = []
            for k,v in temp.items():
                
                senha = v['senha']
                if senha == '':
                    senha = '❌'
                    
                validade = v['validade']
                if validade == '':
                    validade = '❌'
                        
                cvv = v['cvv']
                if cvv == '':
                    cvv = '❌'
                        
                cpf = v['cpf']
                if cpf == '':
                    cpf = '❌'        
                
                telefone = v['telefone']
                if telefone == '':
                    telefone = '❌'        
                
                nome = v['nome']
                if nome == '':
                    nome = '❌'
                
                
                lista.append(f"{v['banco']}\n00 | 00 | --- | --- | {k} | {senha} | {validade} | {cvv} | {cpf} | {telefone} | {nome}\n\n")
            
            if len(lista) < 1:
                return {
                "status": False,
                "message": "❌ Nenhuma consultável identificada"
            }
            
            else:
                        
                arq.salvar_linhas(ca.cache, lista)
                
                retorno = arq.ler_txt(ca.cache)
                
                arq.limpar_txt(ca.cache)

                ''' return {
                    "status": True,
                    "message": retorno
                }'''
                
                return retorno
        else:
            return {
            "status": False,
            "message": "❌ Nenhuma consultável identificada"
        }



def sep_auto_cc(msg, envio = 'normal'):
    qtd_char = len(msg)
    
    msg = msg.splitlines()
    qtd = len(msg)
    
    temp = {}
    
    if envio == 'normal':
        
        if qtd_char > 25:
            
            for c in range(0, qtd):
                try:
                    cc = search_cc(msg[c])
                    validade = search_validade(msg[c])
                    cvv = search_cvv(msg[c])

                    if cc != '❌':
                        temp[cc] = {
                            "cc": cc,
                            "validade": '',
                            "cvv": '',
                        }
                        
                        ultima_cc = cc
                    
                    if validade != '❌':
                        if temp[ultima_cc]['validade'] == '':
                            temp[ultima_cc]['validade'] = validade          
                        
                    if cvv != '❌':
                        if temp[ultima_cc]['cvv'] == '':
                            temp[ultima_cc]['cvv'] = cvv

                    
                except:
                    pass

            lista = []
            for k,v in temp.items():
                    
                validade = v['validade']
                if validade == '':
                    validade = '❌'
                
                cvv = v['cvv']
                        
                if cvv == '':
                    cvv = '❌'
                        
                k = k.replace(' ','')
                lista.append(f"{k}|{validade}|{cvv}\n")
            
            if len(lista) < 1:
                return {
                "status": False,
                "message": "❌ Nenhuma cc identificada"
            }
            
            else:
                arq.salvar_linhas(ca.cache, lista)
                
                retorno = arq.ler_txt(ca.cache)
                
                arq.limpar_txt(ca.cache)
                
                return {
                    "status": True,
                    "message": retorno
                }
        
        else:
            return {
                "status": False,
                "message": "❌ Nenhuma cc identificada"
            }


    else:
        if qtd_char > 25:
            
            for c in range(0, qtd):
                try:
                    cc = search_cc(msg[c])
                    validade = search_validade(msg[c])
                    cvv = search_cvv(msg[c])

                    if cc != '❌':
                        temp[cc] = {
                            "cc": cc,
                            "validade": '',
                            "cvv": '',
                            "bin": '',
                        }
                        
                        ultima_cc = cc
                        
                        bin_cc = cc.replace(" ", "")[:6]
                        bin_atual = bin.checker(bin_cc)
                    
                        if bin_atual['status'] == 'ok':
                            info_bin = f"{bin_atual['bandeira']}|{bin_atual['tipo']}|{bin_atual['level']}|{bin_atual['banco']}|{bin_atual['pais']}"
                            temp[cc]['bin'] = info_bin
                        
                        else:
                            info_bin = f"INDEFINIDO|INDEFINIDO|INDEFINIDO|INDEFINIDO|INDEFINIDO"
                            temp[cc]['bin'] = info_bin

                        
                    
                    if validade != '❌':
                        if temp[ultima_cc]['validade'] == '':
                            temp[ultima_cc]['validade'] = validade          
                        
                    if cvv != '❌':
                        if temp[ultima_cc]['cvv'] == '':
                            temp[ultima_cc]['cvv'] = cvv

                except:
                    pass

            lista = []
            for k,v in temp.items():
                
                validade = v['validade']
                if validade == '':
                    validade = '❌'
                
                cvv = v['cvv']
                        
                if cvv == '':
                    cvv = '❌'
                        
                k = k.replace(' ','')
                
                lista.append(f"{k}|{validade}|{cvv}|{v['bin']}\n")
            
            if len(lista) < 1:
                return {
                "status": False,
                "message": "❌ Nenhuma cc identificada"
            }
            
            else:
                        
                arq.salvar_linhas(ca.cache, lista)
                
                retorno = arq.ler_txt(ca.cache)
                
                arq.limpar_txt(ca.cache)
                
                return {
                    "status": True,
                    "message": retorno
                }
        else:
            return {
            "status": False,
            "message": "❌ Nenhuma cc identificada"
        }
