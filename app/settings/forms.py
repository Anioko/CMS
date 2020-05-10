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
from wtforms import StringField, SelectField, DateTimeField
#from app.wtform_widgets import MarkdownField
from flask_pagedown.fields import PageDownField
from wtforms.validators import DataRequired, Length
from app.models import BlogCategory
from app.models import BlogPostStatus
from flask_wtf import Form

#from app.models import User


class SiteSettingForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired(), \
                        Length(min=1, max=128)])
    value = StringField("Value", validators=[InputRequired()])
    submit = SubmitField('Submit')
    

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(1, 128)])
    slug = StringField('Slug/Url', validators=[DataRequired(), Length(1, 256)])
    content = PageDownField('Content')
    published_on = DateTimeField('Published On', validators=[DataRequired()])
    category = SelectField('Category', coerce=int)
    status = SelectField('Status', coerce=int)
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

        self.category.choices = [(category.id, category.name)
                                 for category in BlogCategory.query.order_by(BlogCategory.name)]
        self.status.choices = [(status.id, status.name)
                               for status in BlogPostStatus.query.order_by(BlogPostStatus.name)]


class CategoryForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(1, 64)])
    slug = StringField('Slug/Url', validators=[DataRequired(), Length(1, 256)])
    description = StringField("Description", validators=[Length(1, 512)])
    submit = SubmitField('Submit')

class EditCategoryForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(1, 64)])
    slug = StringField('Slug/Url', validators=[DataRequired(), Length(1, 256)])
    description = StringField("Description", validators=[Length(1, 512)])
    submit = SubmitField('Submit')
    
class StatusForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired(), \
                        Length(min=1, max=128)])
    #value = StringField("Value", validators=[InputRequired()])
    submit = SubmitField('Submit')