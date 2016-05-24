from pprint import pprint

from anki.hooks import addHook
from aqt.utils import showInfo

from GenumCore.Collins import Collins, CollinsError
from GenumCore.vendor.yandextranslate import yandex_translate

TRANSLATE_FIELD = 1
FOREIGN_PRONUNCIATION = 5
COLLINS_ACCESS_KEY = 'Enter the collins dictionary key here!'
DICTIONARY_CODE = 'american-learner'

ya_translator = yandex_translate.YandexTranslate(
    key='trnsl.1.1.20160518T163740Z.4a96ea038dcee5ab.1765897e66cff5ec99ed22bf01abfa6e0904b697')
collins = Collins(access_key=COLLINS_ACCESS_KEY, dictionary=DICTIONARY_CODE)


def generate(editor):
    # Get the ForeignWord field.
    editor.loadNote()
    editor.web.setFocus()
    editor.web.eval("focusField(0);")
    editor.web.eval("caretToEnd();")
    word_to_translate = editor.note.fields[0]
    pprint(editor.note)
    # check that ForeignWord is not empty
    if word_to_translate == "":
        showInfo("ForeignWord should not be empty.")
        return

    # Russian translation by Yandex.Translator
    translated = ya_translator.translate(word_to_translate, 'ru')
    if translated['code'] == 200:
        editor.note.fields[TRANSLATE_FIELD] = ", ".join(translated['text'])

    # Working with Collins dictionary:
    try:
        editor.note.fields[FOREIGN_PRONUNCIATION] = collins.get_pronunciation(word=word_to_translate)
    except CollinsError, e:
        showInfo("Warning: " + e.msg)

    # reload the note to display changes
    editor.loadNote()


def setup_buttons(editor):
    editor._addButton("Genum", lambda ed=editor: generate(ed), text="GM", tip="Generate document (Ctrl+g)",
                      key="Ctrl+g")


addHook("setupEditorButtons", setup_buttons)
print("Genum starts")
