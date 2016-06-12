from aqt.utils import showInfo
from Collins import Collins, CollinsError
from YandexDict import YandexDict
from bingsearch.py_bing_search import PyBingImageSearch
from yandextranslate import yandex_translate
import Genum

ya_translator = yandex_translate.YandexTranslate(key=Genum.YANDEX_TRANSLATOR)
ya_dict = YandexDict(api_key=Genum.YANDEX_DICT)
collins = Collins(access_key=Genum.COLLINS_ACCESS_KEY, dictionary=Genum.DICTIONARY_CODE)


def generate(editor):
    if any(key == 'Enter API key here!'
           for key in (Genum.COLLINS_ACCESS_KEY, Genum.BING_API_KEY, Genum.YANDEX_DICT, Genum.YANDEX_TRANSLATOR)):
        showInfo("Please fill API keys. (Tools -> Add-ons -> Genum -> Edit...)")
        return

    # Get the ForeignWord field.
    editor.loadNote()
    editor.web.setFocus()
    editor.web.eval("focusField(0);")
    editor.web.eval("caretToEnd();")
    word_to_translate = editor.note.fields[Genum.TO_TRANSLATE]
    # check that ForeignWord is not empty
    if word_to_translate == "":
        showInfo("ForeignWord should not be empty.")
        return

    # Russian translation by Yandex.Translator
    editor.note.fields[Genum.TRANSLATED_FIELD] = ya_dict.get_definition_by_pos(word_to_translate)

    # Working with Collins dictionary:
    try:
        editor.note.fields[Genum.FOREIGN_PRONUNCIATION] = editor.urlToFile(collins.get_pronunciation(word_to_translate))
        context_list = collins.get_context_list(word_to_translate)
        editor.note.fields[Genum.CONTEXT] = process_list(context_list, word_to_translate)
        editor.note.fields[Genum.CONTEXT] += "<br><br>" + process_list(collins.get_definitions_list(word_to_translate),
                                                                       word_to_translate)
        # TODO: translate by one request and save split by lines (<br> tag)
        translated_context = ya_translator.translate("  ".join(context_list), 'ru')
        if translated_context['code'] == 200:
            editor.note.fields[Genum.CONTEXT_TRANSLATE] = translated_context['text'][0]  # TODO: check for null
        editor.note.fields[Genum.TRANSCRIPTION] = collins.get_transcriptions_list(word_to_translate)[0]
    except CollinsError as e:
        showInfo("Warning: " + e.msg)

    # Working with Bing Search
    image_search_result = PyBingImageSearch(Genum.BING_API_KEY, word_to_translate, image_filters='Size:Medium') \
        .search(limit=1, format='json')
    if image_search_result and image_search_result[0].media_url:
        editor.note.fields[Genum.IMAGE] = editor.urlToFile(image_search_result[0].media_url)

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
