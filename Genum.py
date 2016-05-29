from pprint import pprint

from anki.hooks import addHook
from aqt.utils import showInfo

from GenumCore.Collins import Collins, CollinsError
from GenumCore.vendor.bingsearch.py_bing_search import PyBingImageSearch
from GenumCore.vendor.yandextranslate import yandex_translate

# Card template
TO_TRANSLATE = 0
TRANSLATED_FIELD = 1
CONTEXT_TRANSLATE = 2
CONTEXT = 3
TRANSCRIPTION = 4
FOREIGN_PRONUNCIATION = 5
IMAGE = 6

# Collins dictionary
COLLINS_ACCESS_KEY = 'Enter the collins dictionary key here!'
DICTIONARY_CODE = 'american-learner'

# Bing Search
BING_API_KEY = 'Enter Bing search API key here!'

# Yandex.Translator
ya_translator = yandex_translate.YandexTranslate(
    key='trnsl.1.1.20160518T163740Z.4a96ea038dcee5ab.1765897e66cff5ec99ed22bf01abfa6e0904b697')
collins = Collins(access_key=COLLINS_ACCESS_KEY, dictionary=DICTIONARY_CODE)


def generate(editor):
    # Get the ForeignWord field.
    editor.loadNote()
    editor.web.setFocus()
    editor.web.eval("focusField(0);")
    editor.web.eval("caretToEnd();")
    word_to_translate = editor.note.fields[TO_TRANSLATE]
    pprint(editor.note)
    # check that ForeignWord is not empty
    if word_to_translate == "":
        showInfo("ForeignWord should not be empty.")
        return

    # Russian translation by Yandex.Translator
    translated = ya_translator.translate(word_to_translate, 'ru')
    # TODO: duplication of success check, extract translation by yandex to particular function
    if translated['code'] == 200:
        editor.note.fields[TRANSLATED_FIELD] = ", ".join(translated['text'])

    # Working with Collins dictionary:
    try:
        editor.note.fields[FOREIGN_PRONUNCIATION] = collins.get_pronunciation(word_to_translate)
        context_list = collins.get_context_list(word_to_translate)
        editor.note.fields[CONTEXT] = process_context(context_list, word_to_translate)
        # TODO: translate by one request and save split by lines (<br> tag)
        translated_context = ya_translator.translate("  ".join(context_list), 'ru')
        if translated_context['code'] == 200:
            editor.note.fields[CONTEXT_TRANSLATE] = translated_context['text'][0]  # TODO: check for null
    except CollinsError, e:
        showInfo("Warning: " + e.msg)

    # Working with Bing Search
    image_search_result = PyBingImageSearch(BING_API_KEY, word_to_translate, image_filters='Size:Medium') \
        .search(limit=1, format='json')
    if image_search_result:
        editor.note.fields[IMAGE] = image_search_result[0].media_url

    # reload the note to display changes
    editor.loadNote()


def process_context(context_list, word):
    context_list_bold = [bold_word(context, word) for context in context_list]
    return "<br>".join(context_list_bold)


def bold_word(statement, word):
    words = statement.split()
    for i, w in enumerate(words):
        index = w.find(word)
        if index != -1:
            words[i] = '<b>%s</b>' % w
    return " ".join(words)


def setup_buttons(editor):
    editor._addButton("Genum", lambda ed=editor: generate(ed), text="GM", tip="Generate document (Ctrl+g)",
                      key="Ctrl+g")


addHook("setupEditorButtons", setup_buttons)
print("Genum starts")
