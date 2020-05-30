from flask import Blueprint, render_template, abort, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_required

from app.models import *
from app.contractor.forms import *

contractor = Blueprint('contractor', __name__)



@contractor.route('/add/', methods=['Get', 'POST'])
@login_required
def create_contractor():
    #user_id = contractor.query.filter_by(user_id=current_user.id).filter_by(id=user_id).first_or_404()
    form = ContractorForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            appt = Contractor(start_date=form.start_date.data.strftime('%d-%m-%Y'),
                       user_id=current_user.id,
                       end_date=form.end_date.data.strftime('%d-%m-%Y'),  # ''' ##('%Y-%m-%d') Alternative '''
                       minimum_rate=form.minimum_rate.data,
                       maximum_rate=form.maximum_rate.data,
                       currencies=form.currencies.data,
                       minimum_duration=form.minimum_duration.data,
                       )
            db.session.add(appt)
            db.session.commit()
            flash('contractor details added!', 'success')
            return redirect(url_for('contractor.contractor_details', id=appt.id, minimum_rate=appt.minimum_rate,
                                    maximum_rate=appt.maximum_rate))
        else:

            flash('ERROR! details was not added.', 'error')
    return render_template('contractor/create_contractor.html', form=form)

@contractor.route('/list/')
def contractor_list():
    #appts = contractor.query.filter(contractor.organisation != None).filter(contractor.end_date >= datetime.now()).order_by(contractor.pub_date.asc()).all()
    #return render_template('contractor/allcontractor.html', appts=appts)
    #def contractor_list():
    appts = Contractor.query.all()
    return render_template('contractor/allcontractor.html', appts=appts)




@contractor.route('/<int:id>/<minimum_rate>/<maximum_rate>/')
def contractor_details(id, minimum_rate, maximum_rate):
    appts = Contractor.query.filter(Contractor.id == id).first_or_404()
    org_users = User.query.all()
    orgs = Contractor.query.filter(Contractor.user_id == User.id).all()
    return render_template('contractor/contractor_details.html', appt=appts, orgs=orgs, org_users=org_users)
