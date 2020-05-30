from flask import Blueprint, render_template, abort, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_required

from app.models import *
from app.workplace.forms import *

workplace = Blueprint('workplace', __name__)


@workplace.route('/add/', methods=['Get', 'POST'])
@login_required
def create_workplace():
    #user_id = workplace.query.filter_by(user_id=current_user.id).filter_by(id=user_id).first_or_404()
    form = WorkplaceForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            appt = Workplace(start_date=form.start_date.data.strftime('%d-%m-%Y'),  # ''' ##('%Y-%m-%d') Alternative '''
                       user_id=current_user.id,
                       end_date=form.end_date.data.strftime('%d-%m-%Y'),  # ''' ##('%Y-%m-%d') Alternative '''
                       name=form.name.data,
                       role=form.role.data,
                       currently=form.currently.data,
                       description=form.description.data,
                       role_description=form.role_description.data,
                       city=form.city.data,
                       state=form.state.data,
                       country=form.country.data,
                       )
            db.session.add(appt)
            db.session.commit()
            flash('workplace details added!', 'success')
            return redirect(url_for('workplace.workplace_details', id=appt.id, name=appt.name,
                                    city=appt.city, state=appt.state,
                                    country=appt.country))
        else:

            flash('ERROR! details was not added.', 'error')
    return render_template('workplace/create_workplace.html', form=form)

@workplace.route('/list/')
def workplace_list():
    #appts = workplace.query.filter(workplace.organisation != None).filter(workplace.end_date >= datetime.now()).order_by(workplace.pub_date.asc()).all()
    #return render_template('workplace/allworkplace.html', appts=appts)
    #def workplace_list():
    appts = Workplace.query.all()
    return render_template('workplace/allworkplace.html', appts=appts)




@workplace.route('/<int:id>/<name>/<city>/<state>/<country>/')
def workplace_details(id, name, city, state, country):
    appts = workplace.query.filter(Workplace.id == id).first_or_404()
    org_users = User.query.all()
    orgs = Workplace.query.filter(Workplace.user_id == User.id).all()
    return render_template('workplace/workplace_details.html', appt=appts, orgs=orgs, org_users=org_users)
