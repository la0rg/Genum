# Card template
# Numbers are used to fill certain field position in a template, if you use custom template please redefine variables
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

# Oxford dictionary
OXFORD_APP_KEY = 'Enter API key here!'
OXFORD_APP_ID = 'Enter API key here!'
# Available regions: 'us' and 'gb'
OXFORD_REGION = 'us'

# Bing Search
BING_API_KEY = 'Enter API key here!'

# Yandex.Translator
YANDEX_TRANSLATOR = "Enter API key here!"
YANDEX_DICT = "Enter API key here!"

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

# create a new menu item for creation of default template, and add it to the tools menu
action = QAction("Create Genum card template...", mw)
action.setIcon(QIcon(':/icons/help-hint.png'))
mw.connect(action, SIGNAL("triggered()"), CardTemplate.create_genum_card_type)
mw.form.menuTools.addAction(action)
