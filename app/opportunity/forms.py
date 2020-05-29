from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, SelectField, TextAreaField, IntegerField
from wtforms.validators import Length, Required

class OpportunityForm(FlaskForm):    
###Opportunity form for both contractors and employment seekers to fill out
    title = StringField(' Title for what you are looking for')
    summary = StringField(' Write a very short summary')
    opportunity_type = SelectField(u'Contractor or Full Time Employment', choices=[('Yes', 'No')])
    available_now = SelectField(u'Available now or later', choices=[('Available', 'Available'), ('Available', 'Available')])
    location_type = SelectField(u'Onsite or Remote', choices=[('Onsite', 'Onsite'), ('Remote', 'Remote')])
    city = StringField('Which City?')
    state = StringField('Which State?')
    country = StringField('Which Country?')
    save = SubmitField('Submit')
