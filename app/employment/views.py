from flask import Blueprint, render_template, abort, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_required

from app.models import *
from app.employment.forms import *

employment = Blueprint('employment', __name__)



@employment.route('/add/', methods=['Get', 'POST'])
@login_required
def create_employment():
    #user_id = employment.query.filter_by(user_id=current_user.id).filter_by(id=user_id).first_or_404()
    form = EmploymentForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            appt = Employment(minimum_pay=form.minimum_pay.data,
                       user_id=current_user.id,
                       maximum_pay=form.maximum_pay.data,
                       currencies=form.currencies.data,
                       minimum_duration=form.minimum_duration.data,
                       )
            db.session.add(appt)
            db.session.commit()
            flash('Employment details added!', 'success')
            return redirect(url_for('employment.employment_details', id=appt.id, minimum_pay=appt.minimum_pay,
                                    maximum_pay=appt.maximum_pay, currencies=appt.currencies))
        else:

            flash('ERROR! details was not added.', 'error')
    return render_template('employment/create_employment.html', form=form)

@employment.route('/list/')
def employment_list():
    #appts = employment.query.filter(employment.organisation != None).filter(employment.end_date >= datetime.now()).order_by(employment.pub_date.asc()).all()
    #return render_template('employment/allemployment.html', appts=appts)
    #def employment_list():
    appts = Employment.query.all()
    return render_template('employment/allemployment.html', appts=appts)




@employment.route('/<int:id>/<minimum_pay>/<maximum_pay>/<currencies>/')
def employment_details(id, minimum_pay, maximum_pay, currencies):
    appts = Employment.query.filter(Employment.id == id).first_or_404()
    org_users = User.query.all()
    orgs = Employment.query.filter(Employment.user_id == User.id).all()
    return render_template('employment/employment_details.html', appt=appts, orgs=orgs, org_users=org_users)
