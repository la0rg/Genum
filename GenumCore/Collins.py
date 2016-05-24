import json

from GenumCore.vendor.collinsapi import collins


class Collins:
    """ Collins encapsulates logic of working with Collins dictionary API"""
    baseUrl = 'https://api.collinsdictionary.com/api/v1/'

    def __init__(self, access_key='default', dictionary='default'):
        self._dictionary = dictionary
        self._access_key = access_key
        self._api = collins.API(baseUrl=Collins.baseUrl,
                                accessKey=access_key)

    def _fields_not_empty(self):
        if self._dictionary == 'default' or self._access_key == 'default':
            raise CollinsError('Access key and dictionary name should be filled.')

    def search_entry_id(self, word):
        self._fields_not_empty()
        entry = json.loads(self._api.search(dictionaryCode=self._dictionary,
                                            searchWord=word, pageSize=1))
        # Return the first word
        return entry['results'][0]['entryId']

    def get_pronunciation(self, word):
        self._fields_not_empty()
        entry_id = self.search_entry_id(word=word)
        pronunciation = json.loads(self._api.getEntryPronunciations(dictionaryCode=self._dictionary,
                                                                    entryId=entry_id,
                                                                    lang='us'))
        return pronunciation[0]['pronunciationUrl']


class CollinsError(RuntimeError):
    def __init__(self, msg):
        self.msg = msg
