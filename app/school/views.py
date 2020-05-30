from flask import Blueprint, render_template, abort, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_required

from app.models import *
from app.school.forms import *

school = Blueprint('school', __name__)


@school.route('/add/', methods=['Get', 'POST'])
@login_required
def create_school():
    #user_id = school.query.filter_by(user_id=current_user.id).filter_by(id=user_id).first_or_404()
    form = SchoolForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            appt = School(start_date=form.start_date.data.strftime('%d-%m-%Y'),  # ''' ##('%Y-%m-%d') Alternative '''
                       user_id=current_user.id,
                       end_date=form.end_date.data.strftime('%d-%m-%Y'),  # ''' ##('%Y-%m-%d') Alternative '''
                       name=form.name.data,
                       currently=form.currently.data,
                       grading=form.grading.data,
                       description=form.description.data,
                       city=form.city.data,
                       state=form.state.data,
                       country=form.country.data,
                       )
            db.session.add(appt)
            db.session.commit()
            flash('School details added!', 'success')
            return redirect(url_for('school.school_details', id=appt.id, name=appt.name,
                                    city=appt.city, state=appt.state,
                                    country=appt.country))
        else:

            flash('ERROR! details was not added.', 'error')
    return render_template('school/create_school.html', form=form)

@school.route('/list/')
def school_list():
    #appts = school.query.filter(school.organisation != None).filter(school.end_date >= datetime.now()).order_by(school.pub_date.asc()).all()
    #return render_template('school/allschool.html', appts=appts)
    #def school_list():
    appts = school.query.all()
    return render_template('school/allschool.html', appts=appts)




@school.route('/<int:id>/<name>/<city>/<state>/<country>/')
def school_details(id, name, city, state, country):
    appts = School.query.filter(school.id == id).first_or_404()
    org_users = User.query.all()
    orgs = School.query.filter(school.user_id == User.id).all()
    return render_template('school/school_details.html', appt=appts, orgs=orgs, org_users=org_users)
