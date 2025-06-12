import requests
import json

url = 'https://guilhermeonrails.github.io/api-restaurantes/restaurantes.json' 

response = requests.get(url)

if response.status_code == 200:
    dados_json = response.json()

    # Estrutura final agrupada por restaurante
    dados_agrupados = []

    # Dicionário temporário para facilitar a agregação
    restaurante_dict = {}

    for item in dados_json:
        nome_restaurante = item['Company']

        if nome_restaurante not in restaurante_dict:
            restaurante_dict[nome_restaurante] = {
                "Company": nome_restaurante,
                "menu": []
            }

        restaurante_dict[nome_restaurante]["menu"].append({
            "item": item["Item"],
            "price": item["price"],
            "description": item["description"]
        })

    # Converter dicionário para lista
    dados_agrupados = list(restaurante_dict.values())

    # Salvar em um único arquivo JSON com encoding UTF-8 e sem escapes Unicode
    with open('cardapio_completo.json', 'w', encoding='utf-8') as arquivo_json:
        json.dump(dados_agrupados, arquivo_json, indent=4, ensure_ascii=False)

    print("Arquivo JSON criado com sucesso!")

else:
    print(f'O erro foi {response.status_code}: {response.text}')