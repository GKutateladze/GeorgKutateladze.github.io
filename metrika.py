import requests
from pprint import pprint
from urllib.parse import urlencode

APP_ID = "ffbbbf50349745ce9d0db0f53a9dedf6"
AUTH_URL = "https://oauth.yandex.ru/authorize"

# auth_data = {
#     'response_type': 'token',
#     'client_id': APP_ID
# }
#
# print('?'.join((AUTH_URL, urlencode(auth_data))))
#
# first_user = {
#     'visits': None,
#     'token': "AQAAAAAiETCRAAToqTLcxJeanUjBu1-O88tzcc8"
# }
#
# TOKEN = "AQAAAAAiETCRAAToqTLcxJeanUjBu1-O88tzcc8"
# SECOND_TOKEN = "second_token"
#
# params = {
#     "oauth_token": first_user['token'],
#     "pretty": 1
# }
#
# response = requests.get("https://api-metrika.yandex.ru/management/v1/counters", params)
# counter_id = response.json()["counters"][0]["id"]
#
#
# params = {
#     "id": counter_id,
#     "metrics": "ym:s:visits"
# }
# headers = {
#     "Authorization": "OAuth {}".format(first_user['token'])
# }
#
#
#
# def get_visits(token, counter_id):
#     params = {
#         "id": counter_id,
#         "metrics": "ym:s:visits"
#     }
#     headers = {
#         "Authorization": "OAuth {}".format(first_user['token'])
#     }
#     response = requests.get("https://api-metrika.yandex.ru/stat/v1/data", params, headers=headers)
#     return response.json()['totals'][0]
#
# first_user['visits'] = get_visits(first_user['token'], counter_id)
# pprint(first_user)


class YaBase:
    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            "Authorization": "OAuth {}".format(self.token)
        }


class YaMetricaUser(YaBase):
    def get_counter(self):
        headers = self.get_headers()

        response = requests.get("https://api-metrika.yandex.ru/management/v1/counters", headers=headers)

        return [Counter(c['id'], self.token) for c in response.json()['counters']]


class Counter(YaBase):
    def __init__(self, counter_id, token):
        self.counter_id = counter_id
        super().__init__(token)

    @property
    def visits(self):
        headers = self.get_headers()
        params = {
            "id": self.counter_id,
            "metrics": "ym:s:visits"
        }

        response = requests.get("https://api-metrika.yandex.ru/stat/v1/data", params, headers=headers)
        try:
            return response.json()['totals']              #['visits'][0]['metrics'][0]?
        except IndexError as e:
            return e

first_user = YaMetricaUser("AQAAAAAiETCRAAToqTLcxJeanUjBu1-O88tzcc8")
counters = first_user.get_counter()
for counter in counters:
    print(counter.counter_id, ":", counter.visits)