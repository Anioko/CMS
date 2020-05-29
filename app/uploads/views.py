import os
from flask import Blueprint, render_template, flash, request, redirect, url_for
#from flask_dropzone import Dropzone
#from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from werkzeug.utils import secure_filename
from flask import send_from_directory

from app.models import EditableHTML
from .forms import FileForm
from app.decorators import admin_required

uploads = Blueprint('uploads', __name__)

#dropzone = Dropzone(uploads)

# Dropzone settings
#uploads.config['DROPZONE_UPLOAD_MULTIPLE'] = True
#uploads.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
#uploads.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*'
#uploads.config['DROPZONE_REDIRECT_VIEW'] = 'results'

#
# photos = UploadSet('photos', IMAGES)
# configure_uploads(uploads, photos)
# patch_request_class(uploads)  # set maximum file size, default is 16MB

UPLOAD_FOLDER = os.getcwd()
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])



@uploads.route('/')
def index():
    return render_template('uploads/index.html')

@uploads.route('/about')
def about():
    editable_html_obj = EditableHTML.get_editable_html('about')
    return render_template(
        'main/about.html', editable_html_obj=editable_html_obj)
        
def allowed_file(filename):
      return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
@uploads.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER,
                               filename)
 
@uploads.route('/single', methods=['GET', 'POST']) 
def upload_file():
    form = FileForm()
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploads.uploaded_file',
                                    filename=filename))
    return render_template('uploads/upload.html', form=form, )
    # '''
    # <!doctype html>
    # <title>Upload new File</title>
    # <h1>Upload new File</h1>
    # <form method=post enctype=multipart/form-data>
    # {{ form.csrf_token }}
      # <input type=file name=file>
      # <input type=submit value=Upload>
    # </form>
    # '''
   
@uploads.route('/multiple')   
def upload_form():
    return render_template('uploads/upload.html')

@uploads.route('/multiple', methods=['POST'])
def upload_multiple_files():
	if request.method == 'POST':
        # check if the post request has the files part
		if 'files[]' not in request.files:
			flash('No file part')
			return redirect(request.url)
		files = request.files.getlist('files[]')
		for file in files:
			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		flash('File(s) successfully uploaded')
		return redirect('/')


@uploads.route('/file', methods=['GET', 'POST'])
@admin_required
def image_upload():
    ''' No checks '''

    form = FileForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            image_filename = images.save(request.files['file'])
            image_url = images.url(image_filename)
            file = Upload(
                    image_filename=image_filename,
                    image_url=image_url
                )
            db.session.add(file)
            db.session.commit()
            flash("Image saved.")
            return redirect(url_for('uploads.uploaded_file', file=file))
        else:
            flash('ERROR! Upload was not saved.', 'error')
    return render_template('uploads/upload.html', form=form)


# @uploads.route('/results')
# def results():
    # return render_template('uploads/results.html')
    
# @app.route('/upload', methods=['GET', 'POST'])
# def upload():
    # if request.method == 'POST' and 'photo' in request.files:
        # filename = photos.save(request.files['photo'])
        # rec = Photo(filename=filename, user=g.user.id)
        # rec.store()
        # flash("Photo saved.")
        # return redirect(url_for('show', id=rec.id))
    # return render_template('uploads/upload.html')

# @app.route('/photo/<id>')
# def show(id):
    # photo = Photo.load(id)
    # if photo is None:
        # abort(404)
    # url = photos.url(photo.filename)
    # return render_template('uploads/show.html', url=url, photo=photo')