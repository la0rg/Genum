from aqt import mw

front = """
        <div class=word>{{word}}</div>
        <div class=transc>[{{transcription}}]</div> \
        [sound:{{sound}}]
        <div class=mid>{{context}}</div>
        <div class=small>{{definition}}</div>
        """
back = """
        {{FrontSide}}
        <hr id=answer>
        <div class=transl>{{translation}}</div>
        <div class=mid>{{context_translation}}</div><br>
        <img style="width:180px" src="{{image}}">
        """
css = """
        .card { font-family: Arial,sans-serif; text-align: center; background-color: #F5F2E7; }
        .word { font-size: 28px; color: purple; }
        .transc { font-size: 16px; color: #317FC0; font-family: Arial Unicode MS; }
        .transl { font-size: 22px; color: purple; margin: 0 0 10px; }
        .small { font-size: 14px; font-style: italic; color: #111111; margin: 10px 0 0; }
        .small b { color:#317FC0 !important; }
        .mid { font-size: 17px; font-style: italic; color: #222222; margin: 10px 0 0; }
        .mid b { color: #317FC0 !important; }
        """
fields_names = ['word',
                'translation',
                'context_translation',
                'context',
                'transcription',
                'sound',
                'image',
                'definition'
                ]


def create_genum_card_type():
    '''
    Create predefined card type and template for Genum addon
    '''
    mm = mw.col.models
    # Create new card model
    new_model = mm.new("Genum")
    new_model['css'] = css
    # Add fields to the model
    for name in fields_names:
        mm.addField(new_model, mm.newField(name))
    # Add new template to the model
    genum_template = mm.newTemplate('GenumTemplate')
    genum_template['qfmt'] = front
    genum_template['afmt'] = back
    mm.addTemplate(m=new_model, template=genum_template)
    mm.add(new_model)
    print("DONE")
