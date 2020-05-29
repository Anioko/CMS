from flask import Blueprint, render_template

from app.models import EditableHTML

contractor = Blueprint('contractor', __name__)


@contractor.route('/')
def index():
    return render_template('contractor/index.html')


@contractor.route('/about')
def about():
    editable_html_obj = EditableHTML.get_editable_html('about')
    return render_template(
        'contractor/about.html', editable_html_obj=editable_html_obj)
