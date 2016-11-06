import logging as log
import os

import Genum
from Utils import *
from aqt.utils import showInfo
from clients.Oxford import Oxford, OxfordError
from clients.YandexDict import YandexDict, YandexDictException
from vendor.bingsearch.py_bing_search import PyBingImageSearch, PyBingImageException
from vendor.yandextranslate import yandex_translate

ya_translator = yandex_translate.YandexTranslate(key=Genum.YANDEX_TRANSLATOR)
ya_dict = YandexDict(api_key=Genum.YANDEX_DICT)
oxford = Oxford(app_id=Genum.OXFORD_APP_ID, app_key=Genum.OXFORD_APP_KEY, region=Genum.OXFORD_REGION)

parent_dir = os.path.abspath(os.path.dirname(__file__))
log.basicConfig(filename=parent_dir + "/genum.log", level=log.WARNING)


def generate(editor):
    if any(key == 'Enter API key here!'
           for key in (Genum.OXFORD_APP_KEY,
                       Genum.OXFORD_APP_ID,
                       Genum.BING_API_KEY,
                       Genum.YANDEX_DICT,
                       Genum.YANDEX_TRANSLATOR)):
        showInfo("Please fill API keys. (Tools -> Add-ons -> Genum -> Edit...)", parent=editor.parentWindow)
        return

    # Get the ForeignWord field.
    editor.loadNote()
    word_to_translate = editor.note.fields[Genum.TO_TRANSLATE]
    # check that ForeignWord is not empty
    if word_to_translate == "":
        showInfo("ForeignWord should not be empty.", parent=editor.parentWindow)
        return

    problems = []

    # Translation by Yandex.Dictionary
    if Genum.TRANSLATED_FIELD != -1:
        try:
            translation = ya_dict.get_definition_by_pos(word_to_translate)
            if translation:
                editor.note.fields[Genum.TRANSLATED_FIELD] = translation
            else:
                log.warning('Cannot find translation for the word: %s' % word_to_translate)
                problems.append('Cannot find translation')
        except YandexDictException as e:
            log.error('Cannot find translation for the word: %s' % word_to_translate)
            log.error(e.msg)
            problems.append('Cannot find translation')

    # Pronunciation, contexts, definitions and transcription by Oxford dictionary
    context_list = None
    try:
        if Genum.FOREIGN_PRONUNCIATION != -1:
            pronunciation_url = oxford.get_pronunciation(word_to_translate)
            if pronunciation_url:
                link = editor.urlToFile(pronunciation_url)
                if link:
                    editor.note.fields[Genum.FOREIGN_PRONUNCIATION] = link
            else:
                log.warning('Cannot find pronunciation for the word: %s' % word_to_translate)
                problems.append('Cannot find pronunciation')

        if Genum.CONTEXT != -1:
            context_list = oxford.get_contexts(word_to_translate)
            if context_list:
                context_list = cut_list(context_list, Genum.NUMBER_OF_EXAMPLES)
                editor.note.fields[Genum.CONTEXT] = process_list(context_list, word_to_translate)
            else:
                log.warning('Cannot find examples (contexts) for the word: %s' % word_to_translate)
                problems.append('Cannot find examples (contexts)')

        if Genum.DEFINITION != -1:
            definition_list = oxford.get_definitions(word_to_translate)
            if definition_list:
                definition_list = cut_list(definition_list, Genum.NUMBER_OF_DEFINITIONS)
                editor.note.fields[Genum.DEFINITION] = process_list(definition_list, word_to_translate)
            else:
                log.warning('Cannot find definitions for the word: %s' % word_to_translate)
                problems.append('Cannot find definitions')

        if Genum.TRANSCRIPTION != -1:
            transcription = oxford.get_transcription(word_to_translate)
            if transcription:
                editor.note.fields[Genum.TRANSCRIPTION] = transcription
            else:
                log.warning('Cannot find transcription for the word: %s' % word_to_translate)
                problems.append('Cannot find transcription')

    except OxfordError as e:
        log.warning(e.msg)
        problems.append('Cannot get info from the Oxford dictionary')

    # Translate contexts (examples) by Yandex translator
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

    # Image by Bing
    if Genum.IMAGE != -1:
        try:
            bing = PyBingImageSearch(Genum.BING_API_KEY, word_to_translate, image_filters='Size:Medium')
            image = bing.search(limit=1, format='json')
            if image and image[0].media_url:
                url = editor.urlToFile(image[0].media_url)
                if url:
                    editor.note.fields[Genum.IMAGE] = url
            else:
                log.warning('Cannot find image for the word: %s' % word_to_translate)
                problems.append('Cannot find image')
        except PyBingImageException as e:
            log.error('Cannot find image')
            log.error(e.message)
            problems.append('Cannot find image')

    if len(problems) > 0:
        showInfo(process_list(problems, ""), parent=editor.parentWindow)

    # Note somehow lose the word to translate. And we need to put it in the list again.
    editor.note.fields[Genum.TO_TRANSLATE] = word_to_translate

    # reload the note to display changes
    editor.loadNote()
