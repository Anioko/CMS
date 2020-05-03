from flask import url_for
from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms.fields import (
    BooleanField,
    StringField,
    SubmitField,
)
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, EqualTo, InputRequired, Length



class SiteSettingForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired(), \
                        Length(min=1, max=128)])
    value = StringField("Value", validators=[InputRequired()])
    submit = SubmitField('Submit')