from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, SelectField, TextAreaField, IntegerField
from wtforms.validators import Length, Required

class OpportunityForm(FlaskForm):    
###Opportunity form for both contractors and employment seekers to fill out
    title = StringField(' Title for what you are looking for')
    summary = StringField(' Write a very short summary')
    opportunity_type = SelectField(u'Type', choices=[('Contract', 'Contract'), ('Permanent', 'Permanent')])
    location_type = SelectField(u'Onsite or Remote', choices=[('Onsite', 'Onsite'), ('Remote', 'Remote')])
    available_now = SelectField(u'Availability?', choices=[('Now', 'Now'), ('Later', 'Later')])
    city = StringField('Which City?')
    state = StringField('Which State?')
    country = StringField('Which Country?')
    save = SubmitField('Submit')
