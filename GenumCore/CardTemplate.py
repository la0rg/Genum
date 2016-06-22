from aqt import mw

front = """<div class=word>{{word}}</div>
            <div class=transc>[{{transcription}}]</div>
            [sound:{{sound}}]
            <div class=cont>{{context}}</div>
            <div class=cont>{{definition}}</div>
        """
back = """
            {{FrontSide}}
            <hr id=answer>
            <div class=transl>{{translation}}</div>
            <div class=cont>{{context_translation}}</div>
            <img src=\"{{image}}\">
        """
css = """
        .card {
            font-family: Arial,sans-serif;
            text-align: center;
            background-color: #F5F2E7; }
        .word { font-size: 28px; color: #333333; }
        .transc { font-size: 16px; color: #317FC0; font-family: Arial Unicode MS; }
        .transl { font-size: 22px; color: #995B36; margin: 0 0 10px; }
        .cont { font-size: 15px; font-style: italic; color: #666666; margin: 10px 0 0; } .cont b { color: green !important; }
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
