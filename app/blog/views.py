from flask import Blueprint, render_template

from app.models import EditableHTML

blog = Blueprint('blog', __name__)


@blog.route('/')
def index():
    return render_template('main/index.html')


@blog.route('/about')
def about():
    editable_html_obj = EditableHTML.get_editable_html('about')
    return render_template(
        'blog/about.html', editable_html_obj=editable_html_obj)
