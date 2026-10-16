import random
import string
import arq
import ca
import db

import time

def random_char(y):
    gerado = str(random.randint(10,99)).join(random.choice(string.ascii_letters).upper()
        for x in range(y))
    return gerado
    
def gerar_gift():
    global random_char
    gerador = (f'{random_char(2)}_{random_char(2)}_{random_char(2)}_{random_char(2)}')
    return gerador

def salvar_gift(valor=0):

        valor = int(valor)
        gg = gerar_gift()
        
        arq.att_json(ca.gifts, valor, 2, 'novos', gg)
        
        return {
            "status": True,
            "gift": f"/resgatar {gg}",
            "valor":valor
        }


def resgatar_gift(id, gift):
    cliente = db.cliente(id)

    if cliente != False:
        if len(gift) == 19:
            
            if gift not in arq.ler_json(ca.gifts)['usados']:
                if gift in arq.ler_json(ca.gifts)['novos']:
                    valor = arq.ler_json(ca.gifts)['novos'][gift]
                    
                    anterior = cliente['saldo']
                    
                    cliente['saldo'] = anterior + valor
                    
                    # Atualiza o saldo
                    
                    db.atualiza_cadastro(cliente)
                    
                    # Exclui gift dps de resgatado
                    arq.del_json(ca.gifts, 2, 'novos', gift)
                    arq.att_json(ca.gifts, valor, 2, 'usados', gift)
                    
                    return {
                        "status": True,
                        "gift": gift,
                        "valor": valor,
                    }
                
                else:
                    return {
                        "status": False,
                        "message": "Gift não encontrado",
                    }
            else:
                return {
                    "status": False,
                    "message": "Gift já regatado, não é possível regata-lo novamente",
                }
        
        else:
            return {
                "status": False,
                "message": f"Gift inválido, os Gifts são parecidos com {gerar_gift()}",
                }   
                 
    else:
        return {
            "status": False,
            "message": "ID não encontrado",
            
        }
        
