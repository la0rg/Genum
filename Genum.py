# Card template
# You can use -1 to not put result anywhere
# ex.: IMAGE = -1 (if you do not want to get picture)
TO_TRANSLATE = 0  # Word that will be translated
TRANSLATED_FIELD = 1
CONTEXT_TRANSLATE = 2
CONTEXT = 3
TRANSCRIPTION = 4
FOREIGN_PRONUNCIATION = 5
IMAGE = 6
DEFINITION = 7

# Parameters
NUMBER_OF_EXAMPLES = 2  # How many context statements would be (number of context translations will be the same)
NUMBER_OF_DEFINITIONS = 2  # How many definitions in the original language would be

# Collins dictionary
COLLINS_ACCESS_KEY = 'Enter API key here!'
DICTIONARY_CODE = 'american-learner'

# Bing Search
BING_API_KEY = 'Enter API key here!'

# Yandex.Translator
YANDEX_TRANSLATOR = "trnsl.1.1.20160518T163740Z.4a96ea038dcee5ab.1765897e66cff5ec99ed22bf01abfa6e0904b697"
YANDEX_DICT = "dict.1.1.20160529T105443Z.487dc552af9569ab.fff2fb073ab287a5f5d843318bc8fcf1a000cf3f"

import os
import sys

# add vendor directory to module search path
parent_dir = os.path.abspath(os.path.dirname(__file__))
genum_core_dir = os.path.join(parent_dir, 'GenumCore')
vendor_dir = os.path.join(genum_core_dir, 'vendor')
sys.path.append(genum_core_dir)
sys.path.append(vendor_dir)

from aqt import mw
from anki.hooks import addHook
from aqt.qt import *
from GenumCore import Core
from GenumCore import CardTemplate


def setup_buttons(editor):
    editor._addButton("help-hint", lambda ed=editor: Core.generate(ed), tip="Genum start (Ctrl+g)",
                      key="Ctrl+g")

# add Genum button to the editor form
addHook("setupEditorButtons", setup_buttons)

# create a new menu item, and add it to the tools menu
action = QAction("Create Genum card template...", mw)
action.setIcon(QIcon(':/icons/help-hint.png'))
mw.connect(action, SIGNAL("triggered()"), CardTemplate.create_genum_card_type)
mw.form.menuTools.addAction(action)
