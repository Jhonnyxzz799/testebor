import random, time, requests


def pre_auth(cc):
    keys = [
        "eYlQFn4125Jzx9lEreAx-cHJpdmtleQ",
        "y4QSIRvPbKVtcY6I=cHw-cHJpdmtleQ"
    ]

    try:

        key = random.choice(keys)
        r = requests.get(f'https://api2.validcc.pro/?key={key}&cc={cc}')
        r = r.json()
        if r['code'] == "error":

            if r['message'] == False:
                return {
                    "status": False,
                    "live": False,
                    "message": "Sem retorno do checker"
                }

            if "incorrect." in r['message']:
                return {
                    "status": True,
                    "live": False,
                    "message": r['message']
                }
                
            else:
                return {
                    "status": False,
                    "live": False,
                    "message": r['message']
                }

        else:
            if 'live' in r['status'].lower():
                return {
                    "status": True,
                    "live": True,
                    "message": r['status']
                }

            if 'invalid' in r['status'].lower():
                return {
                    "status": True,
                    "live": False,
                    "message": r['status']
                }


            if 'dead' in r['status'].lower():
                return {
                    "status": True,
                    "live": False,
                    "message": r['status']
                }

                

    except Exception as e:
        return {
                "status": False,
                "live": False,
                "message": 'Erro ao se conectar ao checker'
                }


#print(pre_auth('6505070018610931|10|2024|307'))
