from flask_wtf import FlaskForm, csrf
from wtforms import TextField, SubmitField
from wtforms.validators import DataRequired, Length

class SubmitForm(FlaskForm):
    url = TextField(
        'Please enter the url of your Github repository: <br>', validators=[DataRequired()]
    )
    submit = SubmitField('Submit')