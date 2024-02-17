import requests
import pandas as pd
import re

# utilizamos

url = "https://api-usuario.educacaoadventista.org.br/api/v1/encontre-uma-escola/localizacao"

payload = ""
headers = {
    "authority": "api-usuario.educacaoadventista.org.br",
    "accept": "application/json, text/plain, */*",
    "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "origin": "https://www.encontreumaescola.com.br",
    "referer": "https://www.encontreumaescola.com.br/",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
}

response = requests.request("GET", url, data=payload, headers=headers)
json_res = response.json()

nome_colegio = []
latitude = []
longitude = []
for i in range(len(json_res['result']['data'])):
    escola = json_res['result']['data'][i]['urlEscola']
    lat = json_res['result']['data'][i]['latitude']
    lon = json_res['result']['data'][i]['longitude']
    
    nome_colegio.append(escola)
    latitude.append(lat)
    longitude.append(lon)


data = {'Nome_Colegio': nome_colegio, 'Latitude': latitude, 'Longitude': longitude}
df = pd.DataFrame(data)

df = df[~df['Latitude'].isna()]



