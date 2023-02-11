import mercadopago, pytz, datetime, json, requests, time

token = "APP_USR-SEU_TOKEN_MP"

def expiration():
    with open('config/config.json', 'r') as file:
        config = json.loads(file.read())
        expiration_payment = config['expiration_payment_in_minutes']
    
    time_change = datetime.timedelta(minutes=int(expiration_payment))
    new_time = datetime.datetime.now() + time_change

    tz = pytz.timezone("America/Bahia")
    aware_dt = tz.localize(new_time)

    a = aware_dt.isoformat()
    
    return a[:23]+a[26:]

def gerar_pagamento(valor):
        sdk = mercadopago.SDK("APP_USR-SEU_TOKEN_MP")
        payment_data = {
            "transaction_amount": float(str(valor)+'.00'),
            "description": "CONTA PREMIUM",
            "payment_method_id": "pix",
            "payer": {
                "email": 'pedrosabtos28222@gmail.com',
                "first_name": '',
                "last_name": '',
                "identification": {
                    "type": "CPF",
                    "number": ''
                },
                "address": {
                    "zip_code": '',
                    "street_name": '',
                    "street_number": '',
                    "neighborhood": '',
                    "city": '',
                    "federal_unit": ''
                }
            }
        }

        payment_response = sdk.payment().create(payment_data)
        payment = payment_response["response"]

        id_p = str(payment["id"])
        pix = payment['point_of_interaction']['transaction_data']['qr_code']
        return id_p, pix

def status(id_a):
  try:
        with open('config/config.json', 'r') as file:
          config = json.loads(file.read())

        expiration_payment = config['expiration_payment_in_minutes']
        headers = {"Authorization": f"Bearer {token}"}
        contador = 0
        while True:
            contador += 1
            
            request = requests.get(f'https://api.mercadopago.com/v1/payments/{id_a}', headers=headers).json()
            status = str(request['status']).strip()
            if not contador > int(expiration_payment):
                if status == 'pending':
                    pass
                    
                elif status == 'approved':
                    r = 1
                    break
                
                time.sleep(60)
                
            else:
                r = 0
                break

        if r == 1:
            return True
        
        else:
            return False

  except:
        return 'Erro'

