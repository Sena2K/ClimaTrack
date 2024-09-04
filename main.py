import requests
import json
import time
import os

# Dicionário com as 27 capitais do Brasil e seus respectivos IDs de estações meteorológicas
capitais = {
    "São Paulo": "83779",
    "Rio de Janeiro": "83755",
    "Belo Horizonte": "83587",
    "Brasília": "83377",
    "Salvador": "86678",
    "Fortaleza": "82398",
    "Curitiba": "83842",
    "Manaus": "82332",
    "Recife": "82899",
    "Belém": "82191",
    "Porto Alegre": "83967",
    "Goiânia": "83423",
    "São Luís": "82280",
    "Maceió": "81998",
    "Natal": "82598",
    "Teresina": "82579",
    "João Pessoa": "82798",
    "Aracaju": "83096",
    "Cuiabá": "86705",
    "Campo Grande": "86810",
    "Florianópolis": "86958",
    "Macapá": "82099",
    "Palmas": "86607",
    "Boa Vista": "82022",
    "Porto Velho": "82824",
    "Rio Branco": "82915",
    "Vitória": "83648"
}


# Função para obter dados climáticos por hora de uma estação
def get_weather_data(station_id, start_date, end_date, tz):
    url = f"https://d.meteostat.net/app/proxy/stations/hourly?station={station_id}&tz={tz}&start={start_date}&end={end_date}"
    headers = {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()  # Retorna o JSON da resposta
    else:
        return None


# Função para gerar o intervalo de datas de cada mês
def generate_date_ranges():
    date_ranges = [
        ("2024-01-01", "2024-01-31"),
        ("2024-02-01", "2024-02-29"),  # Ano bissexto
        ("2024-03-01", "2024-03-31"),
        ("2024-04-01", "2024-04-30"),
        ("2024-05-01", "2024-05-31"),
        ("2024-06-01", "2024-06-30"),
        ("2024-07-01", "2024-07-31"),
        ("2024-08-01", "2024-08-31")
    ]
    return date_ranges


# Função para salvar os dados em um arquivo JSON por mês
def save_weather_data_to_json(month, data):
    # Cria um diretório para salvar os arquivos, se não existir
    if not os.path.exists('dados_climaticos'):
        os.makedirs('dados_climaticos')

    filename = f"dados_climaticos/clima_{month}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)  # Adiciona ensure_ascii=False
    print(f"Dados de {month} salvos em {filename}")


# Laço para iterar sobre as capitais e buscar dados de cada mês
date_ranges = generate_date_ranges()

for start_date, end_date in date_ranges:
    all_data_for_month = {}
    for capital, station_id in capitais.items():
        tz = "America/Sao_Paulo"  # Pode ajustar a timezone conforme necessário
        data = get_weather_data(station_id, start_date, end_date, tz)
        if data and "data" in data:
            all_data_for_month[capital] = data["data"]  # Adiciona os dados da capital ao dicionário
        else:
            print(f"Erro ao buscar dados de {capital} para o período {start_date} a {end_date}")

    # Salva todos os dados coletados no mês
    month_name = start_date.split("-")[1]  # Extrai o nome do mês
    save_weather_data_to_json(month_name, all_data_for_month)
