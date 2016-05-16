from anki.hooks import addHook, wrap
from aqt.utils import showInfo
from pprint import pprint


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
    for idx, field in enumerate(editor.note.fields):
        editor.note.fields[idx] += " GENUM"

    # reload the note to display changes
    editor.loadNote()


def setup_buttons(editor):
    editor._addButton("Genum", lambda ed=editor: generate(ed), text="GM", tip="Generate document (Ctrl+g)",
                      key="Ctrl+g")


addHook("setupEditorButtons", setup_buttons)
print("Genum starts")
