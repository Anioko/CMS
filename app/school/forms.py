from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, SelectField, TextAreaField, validators
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import Length, Required, ValidationError, InputRequired, Email, Optional



class SchoolForm(Form):    
###Form to add schools attended by professionals (Employees and contractors)
    name = StringField(' Name of the school')
    description = StringField(' Bsc, Msc etc')
    grading = StringField('Your grade')
    start_date = DateField('Start Date:', format='%Y-%m-%d', validators=(validators.Optional(),))
    end_date = DateField('End  Date:', format='%Y-%m-%d', validators=(validators.Optional(),))
    currently = SelectField(u'Currently studying', choices=[('Yes', 'Yes'),('No', 'No') ])
    state = StringField('City')
    city = StringField('State')
    country = StringField('Country')
    save = SubmitField('Submit')
