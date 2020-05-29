import os

from flask import Flask
from flask_assets import Environment
from flask_compress import Compress
from flask_login import LoginManager
from flask_mail import Mail
from flask_rq import RQ
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

from app.assets import app_css, app_js, vendor_css, vendor_js
from config import config as Config
#from flaskext.markdown import Markdown
#from flask_pagedown import PageDown
#from flask_dropzone import Dropzone
#from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class

basedir = os.path.abspath(os.path.dirname(__file__))

mail = Mail()
db = SQLAlchemy()
csrf = CSRFProtect()
compress = Compress()
#pagedown = PageDown()
#dropzone = Dropzone()

# Set up Flask-Login
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'account.login'


#Uploads
#UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def create_app(config):
    app = Flask(__name__)
    config_name = config

    if not isinstance(config, str):
        config_name = os.getenv('FLASK_CONFIG', 'default')

    app.config.from_object(Config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    # not using sqlalchemy event system, hence disabling it
   # Dropzone settings
    #app.config['DROPZONE_UPLOAD_MULTIPLE'] = True
    #app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
    #app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*'
    #app.config['DROPZONE_REDIRECT_VIEW'] = 'results'
    # Uploads settings
    #app.config['UPLOADED_PHOTOS_DEST'] = '/uploads/'
    # Uploads settings
    app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/static/uploads'
    app.config['UPLOAD_FOLDER'] = os.getcwd() + '/uploads'
    app.config['UPLOADS_DEFAULT_DEST'] = os.getcwd() + '/static/uploads'


    #photos = UploadSet('photos', IMAGES)
    #configure_uploads(app, photos)
    #patch_request_class(app)  # set maximum file size, default is 16MB

    Config[config_name].init_app(app)

    # Set up extensions
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    compress.init_app(app)
    RQ(app)
    #Markdown(app)
    #pagedown.init_app(app)
    #dropzone.init_app(app)
    

    # Register Jinja template functions
    from .utils import register_template_utils
    register_template_utils(app)

    # Set up asset pipeline
    assets_env = Environment(app)
    dirs = ['assets/styles', 'assets/scripts']
    for path in dirs:
        assets_env.append_path(os.path.join(basedir, path))
    assets_env.url_expire = True

    assets_env.register('app_css', app_css)
    assets_env.register('app_js', app_js)
    assets_env.register('vendor_css', vendor_css)
    assets_env.register('vendor_js', vendor_js)

    # Configure SSL if platform supports it
    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask_sslify import SSLify
        SSLify(app)

    # Create app blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/main')

    from .school import school as school_blueprint
    app.register_blueprint(school_blueprint, url_prefix='/account/school')

    from .workplace import workplace as workplace_blueprint
    app.register_blueprint(workplace_blueprint, url_prefix='/account/workplace')

    from .employment import employment as employment_blueprint
    app.register_blueprint(employment_blueprint, url_prefix='/account/employment')

    from .opportunity import opportunity as opportunity_blueprint
    app.register_blueprint(oppportunity_blueprint, url_prefix='/account/opportunity')


    from .account import account as account_blueprint
    app.register_blueprint(account_blueprint, url_prefix='/account')

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .settings import settings as settings_blueprint
    app.register_blueprint(settings_blueprint, url_prefix='/settings')

    from .pages import pages as pages_blueprint
    app.register_blueprint(pages_blueprint, url_prefix='/')

    from .blog import blog as blog_blueprint
    app.register_blueprint(blog_blueprint, url_prefix='/blog')

    from .uploads import uploads as uploads_blueprint
    app.register_blueprint(uploads_blueprint, url_prefix='/uploads')
    
    return app
