from aqt.utils import showInfo
from Collins import Collins, CollinsError
from YandexDict import YandexDict, YandexDictException
from bingsearch.py_bing_search import PyBingImageSearch, PyBingImageException
from yandextranslate import yandex_translate
import Genum
import logging as log
import os

ya_translator = yandex_translate.YandexTranslate(key=Genum.YANDEX_TRANSLATOR)
ya_dict = YandexDict(api_key=Genum.YANDEX_DICT)
collins = Collins(access_key=Genum.COLLINS_ACCESS_KEY, dictionary=Genum.DICTIONARY_CODE)

parent_dir = os.path.abspath(os.path.dirname(__file__))
log.basicConfig(filename=parent_dir+"/genum.log", level=log.WARNING)
pics = ("jpg", "jpeg", "png", "tif", "tiff", "gif", "svg", "webp")
audio = ("wav", "mp3", "ogg", "flac", "mp4", "swf", "mov", "mpeg", "mkv", "m4a", "3gp", "spx", "oga")


def generate(editor):
    if any(key == 'Enter API key here!'
           for key in (Genum.COLLINS_ACCESS_KEY, Genum.BING_API_KEY, Genum.YANDEX_DICT, Genum.YANDEX_TRANSLATOR)):
        showInfo("Please fill API keys. (Tools -> Add-ons -> Genum -> Edit...)", parent=editor.parentWindow)
        return

    # Get the ForeignWord field.
    editor.loadNote()
    word_to_translate = editor.note.fields[Genum.TO_TRANSLATE]
    # check that ForeignWord is not empty
    if word_to_translate == "":
        showInfo("ForeignWord should not be empty.", parent=editor.parentWindow)
        return

    # Russian translation by Yandex.Dictionary
    if Genum.TRANSLATED_FIELD != -1:
        try:
            translation = ya_dict.get_definition_by_pos(word_to_translate)
            if translation:
                editor.note.fields[Genum.TRANSLATED_FIELD] = translation
            else:
                log.warning("Cannot find translation")
                showInfo("Cannot find translation", parent=editor.parentWindow)
        except YandexDictException as e:
            log.error(e.msg)
            showInfo("Could not find translation for the word", parent=editor.parentWindow)

    # Working with Collins dictionary to get pronunciation, context and definition:
    context_list = None
    try:
        if Genum.FOREIGN_PRONUNCIATION != -1:
            pronunciation_url = collins.get_pronunciation(word_to_translate)
            if pronunciation_url:
                url = editor.urlToFile(cut_url(pronunciation_url))
                if url:
                    editor.note.fields[Genum.FOREIGN_PRONUNCIATION] = url
            else:
                log.warning('Cannot find pronunciation for the word: %s' % word_to_translate)
                showInfo("Cannot find pronunciation", parent=editor.parentWindow)
        if Genum.CONTEXT != -1:
            context_list = collins.get_context_list(word_to_translate)
            if context_list:
                editor.note.fields[Genum.CONTEXT] = process_list(context_list, word_to_translate)
            else:
                log.warning('Cannot find examples(context) for the word: %s' % word_to_translate)
                showInfo("Cannot find examples(context)", parent=editor.parentWindow)
        if Genum.DEFINITION != -1:
            definition_list = collins.get_definitions_list(word_to_translate)
            if definition_list:
                editor.note.fields[Genum.DEFINITION] = process_list(definition_list, word_to_translate)
            else:
                log.warning('Cannot find definitions for the word: %s' % word_to_translate)
                showInfo("Cannot find definitions", parent=editor.parentWindow)
        if Genum.TRANSCRIPTION != -1:
            transcription = collins.get_transcriptions_list(word_to_translate)
            if transcription:
                editor.note.fields[Genum.TRANSCRIPTION] = transcription[0]
            else:
                log.warning('Cannot find transcription for the word: %s' % word_to_translate)
                showInfo("Cannot find transcription", parent=editor.parentWindow)
    except CollinsError as e:
        log.warning(e.msg)
        showInfo("Cannot get info from Collins dictionary", parent=editor.parentWindow)

    # Working with Yandex translator to translate context (examples)
    if context_list and Genum.CONTEXT_TRANSLATE != -1:
        try:
            context_translations = []
            for context in context_list:
                t = ya_translator.translate(context, 'ru')
                if t and t['text']:
                    context_translations.append(t['text'][0])
                else:
                    log.error('Cannot translate: %s' % context)
            translated_context = "<br>".join(context_translations)
            if translated_context:
                editor.note.fields[Genum.CONTEXT_TRANSLATE] = translated_context
            else:
                log.warning("Cannot translate examples. Result array is empty.")
        except yandex_translate.YandexTranslateException as e:
            log.error("Error while working with Yandex translator: " + e.msg)

    # Working with Bing Search
    if Genum.IMAGE != -1:
        try:
            image_search_result = PyBingImageSearch(Genum.BING_API_KEY, word_to_translate, image_filters='Size:Medium') \
                .search(limit=1, format='json')
            if image_search_result and image_search_result[0].media_url:
                url = editor.urlToFile(cut_url(image_search_result[0].media_url))
                if url:
                    editor.note.fields[Genum.IMAGE] = url
            else:
                log.warning('Cannot find image for the word: %s' % word_to_translate)
                showInfo("Cannot find image", parent=editor.parentWindow)
        except PyBingImageException as e:
            log.error(e.msg)

    # Note somehow lose the word to translate. And we need to put it in the list again.
    editor.note.fields[Genum.TO_TRANSLATE] = word_to_translate

    # reload the note to display changes
    editor.loadNote()


def process_list(context_list, word):
    context_list_bold = [bold_word(context, word) for context in context_list]
    return "<br>".join(context_list_bold)


def bold_word(statement, word):
    words = statement.split()
    for i, w in enumerate(words):
        index = w.find(word)
        if index != -1:
            words[i] = '<b>%s</b>' % w
    return " ".join(words)


def cut_url(url):
    # If url do not ends with only media extension it's probably somewhere in the middle and we need to cut this
    ends = url[url.rfind(".") + 1:]
    if ends not in pics + audio:
        for suffix in pics + audio:
            pos = url.rfind(suffix)
            if pos != -1:
                return url[:pos + len(suffix)]
    # If no suffix was found the url is broken, nothing to do with it
    # If url ends with extension it's ok
    return url
