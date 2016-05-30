import flask_wtf
from widgets import * #http://wtforms.readthedocs.org/en/latest/fields.html

class Form(flask_wtf.Form):
    match_id = IntegerField('Match #', buttons=False)
    team_id = IntegerField('Team #', buttons=False)
    #Form Fields
    comments = TextAreaField('', col_md=12)
