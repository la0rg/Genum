import requests


class Oxford:
    """ Oxford encapsulates logic of working with Oxford dictionary API"""

    baseUrl = "https://od-api.oxforddictionaries.com:443/api/v1/"
    lang = 'en'

    def __init__(self, app_key, app_id, region='us'):
        self._app_key = app_key
        self._app_id = app_id
        self._region = region
        self._cache = {}

    def _retrieve(self, word=''):
        url = self.baseUrl + 'entries/' + self.lang + '/' + word.lower() + '/regions=' + self._region
        headers = {
            'app_id': self._app_id,
            'app_key': self._app_key
        }
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            raise OxfordError('Error while working with Oxford dictionary for word: ' + word)
        self._cache[word] = r.json()

    def get_pronunciation(self, word):
        if word not in self._cache:
            self._retrieve(word=word)
        json = self._cache[word]
        audios = list(Oxford.traverse(json, ['results', 'lexicalEntries', 'pronunciations', 'audioFile']))
        if len(audios) > 0:
            return audios[0]
        return None

    def get_transcription(self, word):
        if word not in self._cache:
            self._retrieve(word=word)
        json = self._cache[word]
        transcriptions = list(
            Oxford.traverse(json, ['results', 'lexicalEntries', 'pronunciations', 'phoneticSpelling']))
        if len(transcriptions) > 0:
            return transcriptions[0]
        return None

    def get_contexts(self, word):
        if word not in self._cache:
            self._retrieve(word=word)
        json = self._cache[word]
        return list(Oxford.traverse(json, ['results', 'lexicalEntries', 'entries', 'senses', 'examples', 'text'])) + \
               list(Oxford.traverse(json, ['results', 'lexicalEntries', 'entries', 'senses', 'subsenses', 'examples',
                                           'text']))

    def get_definitions(self, word):
        if word not in self._cache:
            self._retrieve(word=word)
        json = self._cache[word]
        return list(Oxford.traverse(json, ['results', 'lexicalEntries', 'entries', 'senses', 'definitions'], True))

    @staticmethod
    def traverse(obj, fields, last_field_is_list=False):
        """ Generator which traverse through object by fields (every field is deeper by one level) """
        if not last_field_is_list and fields and len(fields) == 1:
            if fields[0] in obj:
                yield obj[fields[0]]
        elif fields and len(fields) > 0:
            if fields[0] in obj:
                for instance in obj[fields[0]]:
                    for instance2 in Oxford.traverse(instance, fields[1:], last_field_is_list):
                        yield instance2
        else:
            yield obj


class OxfordError(RuntimeError):
    def __init__(self, msg):
        self.msg = msg
