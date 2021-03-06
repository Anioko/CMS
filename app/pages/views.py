from flask import Blueprint, render_template, abort

from app.models import EditableHTML, SiteSetting, Page, Menu
import commonmark

pages = Blueprint('pages', __name__)



@pages.route('/', defaults={'slug': ''})
@pages.route('/<path:slug>')
def page(slug):
    """ This is the main route of the site. It handles the index and all other 'static' pages. """

    # Some sensible defaults
    the_page = {'Title': "", 'Content': ""}
    template_path = "pages/index.html"

    # Init menu to a blank one
    menu = Menu

    # Get all the site settings
    site_settings = SiteSetting.query.all()
    settings = {}
    for setting in site_settings:
        settings[setting.name] = setting.value

    # Markdown Parser and Renderer
    parser = commonmark.Parser()
    renderer = commonmark.HtmlRenderer()

    if slug == "":
        home_page = Page.query.filter_by(is_homepage=True).first()
        if home_page is not None:
            parsed = parser.parse(home_page.content)
            rendered = renderer.render(parsed)

            menu = home_page.menu

            the_page = {
                'Title': home_page.title,
                'Content': rendered
            }
    else:
        template_path = "pages/page.html"
        current_page = Page.query.filter_by(slug=slug).first()
        if current_page is None:
            abort(404)

        parsed = parser.parse(current_page.content)
        rendered = renderer.render(parsed)

        menu = current_page.menu

        the_page = {
            'Title': current_page.title,
            'Content': rendered
        }

    # Let's return the page and menu items
    return render_template(template_path, page=the_page, menu=menu,
                           settings=settings)

