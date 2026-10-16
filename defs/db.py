import pymysql
import time
import json
import threading
import sys, os
sys.path.insert(1, './')

from defs import arq, ca

login = "root"
db = arq.ler_json(ca.config)['dono']['db']

banco = ['id', 'user', 'nome', 'saldo', 'pontos', 'compras','gifts', 'referencia', 'notificacao', 'autorizacao', 'ban']
keys_cc = ['cc', 'mes', 'ano', 'cvv', 'bandeira', 'tipo', 'level', 'banco', 'pais', 'cc_chk', 'cc_comp']


'''
CREATE TABLE `clientes` (
  `id` varchar(15) DEFAULT NULL,
  `user` varchar(25) DEFAULT NULL,
  `nome` varchar(50) DEFAULT NULL,
  `saldo` int(11) DEFAULT 0,
  `pontos` int(11) DEFAULT 0,
  `compras` text DEFAULT "",
  `gifts` text DEFAULT "",
  `referencia` varchar(15) DEFAULT "None",
  `notificacao` tinyint(2) DEFAULT 1,
  `autorizacao` tinyint(2) DEFAULT 1,
  `ban` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
'''

'''
CREATE TABLE `cc` (
  `cc` varchar(18) DEFAULT NULL,
  `mes` varchar(2) DEFAULT NULL,
  `ano` varchar(4) DEFAULT NULL,
  `cvv` varchar(4) DEFAULT NULL,
  `bandeira` varchar(20) DEFAULT "INDEFINIDO",
  `tipo` varchar(25) DEFAULT "INDEFINIDO",
  `level` varchar(25) DEFAULT "INDEFINIDO",
  `banco` varchar(50) DEFAULT "INDEFINIDO",
  `pais` varchar(40) DEFAULT "INDEFINIDO",
  `cc_chk` varchar(30) DEFAULT NULL,
  `cc_comp` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
'''

def cadastro(json_cliente):
    global banco
    # Abrimos uma conexão com o banco de dados:
    conexao = pymysql.connect(db=db, user=login)
    lista = []
    
    
    for c in range(0, len(banco)):
        key_banco = banco[c]
        lista.append(json_cliente[key_banco])
        
    keys = ", ".join(banco)
    
    # Cria um cursor:
    cursor = conexao.cursor()

    
    #INSERIR
    inserir = f"INSERT INTO clientes ({keys}) VALUES {tuple(lista)};"   
    
    cursor.execute(inserir)

    
    
    conexao.commit()

    # Finaliza a conexão
    conexao.close()
    

def cadastro_cc(cc):
    global keys_cc
    lista = []
    
    for c in range(0, len(keys_cc)):
        key_cc = keys_cc[c]
        lista.append(cc[key_cc])
        
    keys = ", ".join(keys_cc)

    conexao = pymysql.connect(db=db, user=login)
    cursor = conexao.cursor()    
    #INSERIR
    inserir = f"INSERT INTO cc ({keys}) VALUES {tuple(lista)};"   
    
    comando = cursor.execute(inserir)


    conexao.commit()
    conexao.close()
    

def id_clientes():
    # Abrimos uma conexão com o banco de dados:
    conexao = pymysql.connect(db=db, user=login)
    # Cria um cursor:
    cursor = conexao.cursor()
    
    

    ver = f"SELECT id FROM clientes;"
    cursor.execute(ver)

    result = cursor.fetchall()
    
    lista = []

    for c in range(0, len(result)):
        l = (result[c][0])
        lista.append(l)
    
    conexao.commit()
    conexao.close()
    
    return(lista)    


def cliente(id):
    global banco
    
    # Abrimos uma conexão com o banco de dados:
    conexao = pymysql.connect(db=db, user=login)
    # Cria um cursor:
    cursor = conexao.cursor()
    

    comando = f"SELECT * FROM clientes WHERE id={id};"

    cursor.execute(comando)

    result = cursor.fetchall()

        
    conexao.commit()
    
    if len(result) > 0:
        lista = []
        

        for c in range(0, len(result)):
            l = (result[c][0])
            lista.append(l)
            
        temp = {}
        
        
        for c in range(0,len(result[0])):
            valor = result[0][c]
            chave = banco[c]
            temp[chave]= valor
        
        conexao.close()
        return temp
    

    else: 
        return False

def atualiza_cadastro(json_cliente):
    global banco 
    
        # Abrimos uma conexão com o banco de dados:
    conexao = pymysql.connect(db=db, user=login)
    lista = []
    
    
    for c in range(0, len(banco)):
        key_banco = banco[c]
        lista.append(json_cliente[key_banco])
        
    att = []
    
    for c in range(0, len(banco)):
        att.append(f"{banco[c]}='{lista[c]}'")
    
    
    att = ", ".join(att)
    
    cursor = conexao.cursor()
    #ATUALIZAR
    
    atualizar = f"UPDATE clientes SET {att} WHERE id={json_cliente['id']};"
      
    
    cursor.execute(atualizar)
    
    conexao.commit()
    # Finaliza a conexão
    conexao.close()
    

def clientes_json():
    while True:
        conexao = pymysql.connect(db=db, user=login)
        # Cria um cursor:
        cursor = conexao.cursor()
        
        keys = banco.copy()
        keys2 = ", ".join(keys) 
        
        cursor.execute(f"SELECT {keys2} FROM clientes")
        myresult = cursor.fetchall()

        temp = {}
        temp2 = {}
        for x in range(0,len(myresult)):
            cliete = myresult[x]
            temp2 = {}
            for c in range(0, len(keys)):
                key = keys[c]
                temp2[key] = myresult[x][c]
            
            id = temp2['id']
            temp[id]=temp2
        
        return temp


def ccs_json():
    while True:
        conexao = pymysql.connect(db=db, user=login)
        # Cria um cursor:
        cursor = conexao.cursor()
        
        keys = keys_cc.copy()
        keys2 = ", ".join(keys) 
        
        cursor.execute(f"SELECT {keys2} FROM cc")
        myresult = cursor.fetchall()

        temp = {}
        temp2 = {}
        for x in range(0,len(myresult)):
            cc = myresult[x][0]
            temp2 = {}

            for c in range(0, len(keys)):
                key = keys[c]
                temp2[key] = myresult[x][c]
            
            temp[cc]=temp2

        return temp


def delete_cc(numero):
    global keys_cc

    conexao = pymysql.connect(db=db, user=login)
    cursor = conexao.cursor()
    
    #DELETAR
    delete = f"DELETE FROM cc WHERE cc='{numero}'"
    
    status = cursor.execute(delete)

    conexao.commit()
    conexao.close()
  

def cc_numero(numero):
    global keys_cc
    
    # Abrimos uma conexão com o banco de dados:
    conexao = pymysql.connect(db=db, user=login)
    # Cria um cursor:
    cursor = conexao.cursor()
    

    comando = f"SELECT * FROM cc WHERE cc={numero};"

    cursor.execute(comando)

    result = cursor.fetchall()

        
    conexao.commit()
    
    if len(result) > 0:
        lista = []
        

        for c in range(0, len(result)):
            l = (result[c][0])
            lista.append(l)
            
        temp = {}
        
        
        for c in range(0,len(result[0])):
            valor = result[0][c]
            chave = keys_cc[c]
            temp[chave]= valor
        
        conexao.close()
        return temp
    

    else: 
        return False


def search_banco(busca, level):
    global keys_cc
    
    # Abrimos uma conexão com o banco de dados:
    conexao = pymysql.connect(db=db, user=login)
    # Cria um cursor:
    cursor = conexao.cursor()
    

    comando = f"SELECT * FROM cc"
    cursor.execute(comando)

    result = cursor.fetchall()
    conexao.close() 

    for c in range(0, len(result)-1):

        if busca.upper() == result[c][7] and level.upper() == result[c][6]:
            temp = {}
            for c2 in range(0,len(result[c])):
                valor = result[c][c2]
                chave = keys_cc[c2]
                temp[chave]= valor

            return temp
    
    return False
            
  
def search_level(level):
    global keys_cc
    
    # Abrimos uma conexão com o banco de dados:
    conexao = pymysql.connect(db=db, user=login)
    # Cria um cursor:
    cursor = conexao.cursor()
    

    comando = f"SELECT * FROM cc"
    cursor.execute(comando)

    result = cursor.fetchall()
    conexao.close()

    for c in range(0, len(result)):
        
        if level.upper() == result[c][6]:
            temp = {}
            for c2 in range(0,len(result[c])):
                valor = result[c][c2]
                chave = keys_cc[c2]
                temp[chave]= valor

            return temp
    
    return False  


def search_bin(bin):
    global keys_cc
    
    # Abrimos uma conexão com o banco de dados:
    conexao = pymysql.connect(db=db, user=login)
    # Cria um cursor:
    cursor = conexao.cursor()
    

    comando = f"SELECT * FROM cc"
    cursor.execute(comando)

    result = cursor.fetchall()
    conexao.close()

    for c in range(0, len(result)-1):
        
        if bin == result[c][0][:6]:
            temp = {}
            for c2 in range(0,len(result[c])):
                valor = result[c][c2]
                chave = keys_cc[c2]
                temp[chave]= valor

            return temp
    
    return False


def search_tipo(tipo, level):

    global keys_cc
    
    # Abrimos uma conexão com o banco de dados:
    conexao = pymysql.connect(db=db, user=login)
    # Cria um cursor:
    cursor = conexao.cursor()
    

    comando = f"SELECT * FROM cc"
    cursor.execute(comando)

    result = cursor.fetchall()
    conexao.close()

    for c in range(0, len(result)-1):
        
        if tipo == result[c][5] and level == result[c][6]:
            temp = {}
            for c2 in range(0,len(result[c])):
                valor = result[c][c2]
                chave = keys_cc[c2]
                temp[chave]= valor

            return temp
    
    return False
            

def search_bandeira(bandeira, level):

    global keys_cc
    
    # Abrimos uma conexão com o banco de dados:
    conexao = pymysql.connect(db=db, user=login)
    # Cria um cursor:
    cursor = conexao.cursor()
    

    comando = f"SELECT * FROM cc"
    cursor.execute(comando)

    result = cursor.fetchall()
    conexao.close()

    for c in range(0, len(result)-1):
        
        if bandeira == result[c][4] and level == result[c][6]:
            temp = {}
            for c2 in range(0,len(result[c])):
                valor = result[c][c2]
                chave = keys_cc[c2]
                temp[chave]= valor

            return temp
    
    return False
            


def limpa_db_cc():
    conexao = pymysql.connect(db=db, user=login)
    cursor = conexao.cursor()

    comando = f"TRUNCATE TABLE cc"

    cursor.execute(comando)
    conexao.commit()



print(f"\n # INICIANDO TESTE DE CONEXÃO COM BANCO DE DADOS {db.upper()}\n")
try:
    clientes = len(clientes_json())
    ccs = len(ccs_json())
    print("==================================")
    print(f"| USUÁRIOS: {clientes:<6} | CCS: {ccs:<6} |")
    print("==================================")

    print(f" # CONEXÃO BEM SUCESSIDIDA\n")
except:
    print(" # ERRO NA CONXEXÃO COM BANCO DE DADOS (BOT NÃO INICIADO)\n")
    os._exit(os.X_OK)
