import json

import requests


class YandexDict:
    base_url = 'https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key={}&lang={}'

    def __init__(self, api_key, lang='en-ru'):
        self._url = self.base_url.format(api_key, lang)

    def lookup(self, word):
        url = self._url + '&text=' + word
        resp = requests.request('GET', url)
        if resp and resp.status_code == 200:
            return json.loads(resp.text)
        return

    def get_definition_by_pos(self, word):
        '''
        get definiton of the word for different part of speech
        '''
        json = self.lookup(word)
