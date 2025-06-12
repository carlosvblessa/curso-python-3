import requests

url = "https://economia.awesomeapi.com.br/last/USD-BRL"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    cotacao = float(data['USDBRL']['bid'])

    mensagem = f'U$1 dólar corresponde a R${cotacao:.2f}'
    print(mensagem)
else:
    print(f'O erro foi {response.status_code}: {response.text}')
