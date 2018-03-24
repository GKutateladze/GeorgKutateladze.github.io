import requests

APP_ID = "ffbbbf50349745ce9d0db0f53a9dedf6"
AUTH_URL = "https://oauth.yandex.ru/authorize"

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
            return response.json()['data'][0]['metrics'][0]
        except IndexError as e:
            return e

    @property
    def pageviews(self):
        headers = self.get_headers()
        params = {
            "id": self.counter_id,
            "metrics": "ym:s:pageviews"
        }

        response = requests.get("https://api-metrika.yandex.ru/stat/v1/data", params, headers=headers)
        try:
            return response.json()['data'][0]['metrics'][0]
        except IndexError as e:
            return e

    @property
    def users(self):
        headers = self.get_headers()
        params = {
            "id": self.counter_id,
            "metrics": "ym:s:users"
        }

        response = requests.get("https://api-metrika.yandex.ru/stat/v1/data", params, headers=headers)
        try:
            return response.json()['data'][0]['metrics'][0]
        except IndexError as e:
            return e


first_user = YaMetricaUser("AQAAAAAiETCRAAToqTLcxJeanUjBu1-O88tzcc8")
counters = first_user.get_counter()
for counter in counters:
    print(counter.counter_id, ":", f'Visits: {counter.visits}, Pageviews: {counter.pageviews}, Users: {counter.users}')
