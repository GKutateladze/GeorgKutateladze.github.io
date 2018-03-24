import requests
from pprint import pprint
from urllib.parse import urlencode

APP_ID = "ffbbbf50349745ce9d0db0f53a9dedf6"
AUTH_URL = "https://oauth.yandex.ru/authorize"

auth_data = {
    'response_type': 'token',
    'client_id': APP_ID
}

print('?'.join((AUTH_URL, urlencode(auth_data))))

TOKEN = "AQAAAAAiETCRAAToqTLcxJeanUjBu1-O88tzcc8"


params = {
    "oauth_token": TOKEN,
    "pretty": 1
}

response = requests.get("https://api-metrika.yandex.ru/management/v1/counters", params)
counter_id = response.json()["counters"][0]["id"]

params = {
    "id": counter_id,
    "metrics": "ym:s:visits"
}

headers = {
    "Authorization": "OAuth {}".format(TOKEN)
}

response = requests.get("https://api-metrika.yandex.ru/stat/v1/data", params, headers=headers)
pprint(response.json())