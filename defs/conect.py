import sqlite3
import json
import arq
import db
from threading import Thread as th

database = "./defs/database.db"

def convert_users( json_str = True ):
    conn = sqlite3.connect( database )
    conn.row_factory = sqlite3.Row # This enables column access by name: row['column_name'] 
    base = conn.cursor()

    rows = base.execute('''
    SELECT * from usuarios
    ''').fetchall()

    conn.commit()
    conn.close()

    usuarios = [dict(ix) for ix in rows]
    
    for c in range(len(usuarios)-1):
        
        print(usuarios[c]['id_user'] , usuarios[c]['nome'], usuarios[c]['saldo'])
            
        try:
        
            temp = {}

            temp['id'] = usuarios[c]['id_user']
            temp['user'] = "@None"
            temp['nome'] = usuarios[c]['nome']
            temp['saldo'] = int(usuarios[c]['saldo'])
            temp['pontos'] = 0
            temp['compras'] = ""
            temp['gifts'] = ""
            temp['autorizacao'] = True
            temp['notificacao'] = True
            temp['ban'] = 0
            temp['referencia'] = "None"
            db.cadastro(temp)
        except:
            print('ERRO')
            pass
        
    print('')
    print('FINALIZADO')

def convert_ccs( json_str = True ):
    conn = sqlite3.connect( database )
    conn.row_factory = sqlite3.Row # This enables column access by name: row['column_name'] 
    base = conn.cursor()

    rows = base.execute('''
    SELECT * from cc
    ''').fetchall()

    conn.commit()
    conn.close()

    ccs = [dict(ix) for ix in rows]
    
    lista = []
    
    for c in range(len(ccs)-1):
        
        if ccs[c]["comprador"] == "None":
            
            cc = f"{ccs[c]['numero']} {ccs[c]['expiracao']} {ccs[c]['cvv']}"
            
            lista.append(cc)
    qtd = len(lista)
    lista = "\n".join(lista)
    arq.salvar_txt('ccs_temp.txt', lista)
    print('')
    print(f'{qtd} CCS FORAM ENVIADAS PARA O BANCO DE DADOS')

print("INICIANDO PROCESSO DE CONVERSÃO")

th(target=convert_users).start()

th(target=convert_ccs).start()

print("PROCESSO DE CONVERSÃO FINALIZADO")