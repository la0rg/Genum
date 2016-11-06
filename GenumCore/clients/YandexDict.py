import json

import requests


class YandexDictException(Exception):
    def __init__(self, msg):
        self.msg = msg


class YandexDict:
    base_url = 'https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key={}&lang={}'

    def __init__(self, api_key, lang='en-ru'):
        self._url = self.base_url.format(api_key, lang)

    def lookup(self, word):
        url = self._url + '&text=' + word
        try:
            resp = requests.request('GET', url)
            if resp and resp.status_code == 200:
                return json.loads(resp.text)
            else:
                raise Exception()
        except Exception:
            raise YandexDictException("YandexDictError while trying to lookup: %s" % word)

    def get_definition_by_pos(self, word):
        '''
        get definiton of the word for different part of speech
        '''
        result = ''
        json = self.lookup(word)
        if json:
            defenitions = json['def']
            # Go through all parts of speech
            for definition in defenitions:
                result += "<span style=\"color:gray;font-size:16px;font-style:italic;\">" + \
                          definition['pos'][:4] + \
                          ':</span> '
                # No more than three translations for one part of speech
                translations = [translation['text'] for translation in definition['tr'][:3]]
                result += ", ".join(translations)
                result += "; "
        return result
