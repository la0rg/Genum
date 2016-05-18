from pprint import pprint

from anki.hooks import addHook
from aqt.utils import showInfo

from GenumCore.vendor.pythonyandextranslate import yandex_translate

translator = yandex_translate.YandexTranslate(
    key='trnsl.1.1.20160518T163740Z.4a96ea038dcee5ab.1765897e66cff5ec99ed22bf01abfa6e0904b697')
TRANSLATE_FIELD = 1


def generate(editor):
    # Get the ForeignWord field.
    editor.loadNote()
    editor.web.setFocus()
    editor.web.eval("focusField(0);")
    editor.web.eval("caretToEnd();")
    fields = editor.note.fields
    pprint(editor.note)
    # check that ForeignWord is not empty
    if fields[0] == "":
        showInfo("ForeignWord should not be empty.")
        return

    # populate fields
    # for idx, field in enumerate(editor.note.fields):
    #     editor.note.fields[idx] += " GENUM"
    translated = translator.translate(fields[0], 'ru')
    if translated['code'] == 200:
        editor.note.fields[TRANSLATE_FIELD] = ", ".join(translated['text'])

    # reload the note to display changes
    editor.loadNote()


def setup_buttons(editor):
    editor._addButton("Genum", lambda ed=editor: generate(ed), text="GM", tip="Generate document (Ctrl+g)",
                      key="Ctrl+g")


addHook("setupEditorButtons", setup_buttons)
print("Genum starts")
