import json

from bs4 import BeautifulSoup

from GenumCore.vendor.collinsapi import collins


class Collins:
    """ Collins encapsulates logic of working with Collins dictionary API"""
    baseUrl = 'https://api.collinsdictionary.com/api/v1/'

    def __init__(self, access_key='default', dictionary='default'):
        self._html_cache = {}  # Save parsed html (soup)
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
        # self._fields_not_empty()
        # entry_id = self.search_entry_id(word=word)
        # pronunciation = json.loads(self._api.getEntryPronunciations(dictionaryCode=self._dictionary,
        #                                                            entryId=entry_id,
        #                                                            lang='us'))
        soup = self._get_html_content(word)
        elements = soup.select("audio > source")
        result = ''
        if elements and elements[0]['src']:
            result = elements[0]['src']
        return result  # .replace('https://api.collinsdictionary.com/media/sounds/',
        #        'http://www.collinsdictionary.com/')

    def get_context_list(self, word):
        return self.get_items_from_html(word, _class='quote')

    def get_definitions_list(self, word):
        return self.get_items_from_html(word, _class='def', limit=3)

    def get_transcriptions_list(self, word):
        return [item.replace('Your browser does not support HTML5 audio.', '')
                for item in self.get_items_from_html(word, _class='pron')]

    def get_items_from_html(self, word, _class='', tag='span', limit=2, ):
        soup = self._get_html_content(word)
        elements = soup.findAll(tag, _class)
        if len(elements) > limit:
            elements = elements[:limit]
        return [element.get_text() for element in elements]

    def _get_html_content(self, word):
        if word in self._html_cache:
            return self._html_cache[word]
        self._fields_not_empty()
        result = json.loads(self._api.searchFirst(dictionaryCode=self._dictionary,
                                                  searchWord=word))
        if not result or not result['entryContent']:
            raise CollinsError('Error on trying to get html content from Collins dictionary: ' + word)
        self._html_cache[word] = BeautifulSoup(result['entryContent'], 'html.parser')
        return self._html_cache[word]


class CollinsError(RuntimeError):
    def __init__(self, msg):
        self.msg = msg
