from app.models import *
#from flask_ckeditor import CKEditorField
from flask_uploads import UploadSet, IMAGES
from flask_wtf import Form, FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import IntegerField, StringField, SubmitField, DateField, TextAreaField, FormField, MultipleFileField, \
    RadioField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Required, ValidationError, InputRequired, Email
from wtforms_alchemy import Unique, ModelForm
from wtforms_alchemy import model_form_factory
BaseModelForm = model_form_factory(FlaskForm)

images = UploadSet('images', IMAGES)
docs = UploadSet('docs', ('rtf', 'odf', 'ods', 'gnumeric', 'abw', 'doc', 'docx', 'xls', 'xlsx', 'pdf'))


class FileForm(FlaskForm):
    file = FileField('Image file', validators=[FileRequired(), FileAllowed(images, 'Images only!')])
    submit = SubmitField('Submit')