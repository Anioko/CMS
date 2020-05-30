from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, SelectField, TextAreaField, validators
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import Length, Required, ValidationError, InputRequired, Email, Optional

class WorkplaceForm(FlaskForm):    
###Form to add workpace by professionals (Employees and contractors)
    name = StringField(' Name of the organization')
    description = StringField(' Anything else you want to include')
    role = StringField('Type of role')
    role_description = StringField('Role Description')
    start_date = DateField('Start Date:', format='%Y-%m-%d', validators=(validators.Optional(),))
    end_date = DateField('End  Date:', format='%Y-%m-%d', validators=(validators.Optional(),))
    currently = SelectField(u'Currently', choices=[('Yes', 'Yes'),('No', 'No') ])
    city = StringField('City')
    state = StringField('State')
    country = StringField('Country')
    save = SubmitField('Submit')
