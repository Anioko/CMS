from flask import Blueprint, render_template, abort, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_required

from app.models import *

opportunity = Blueprint('opportunity', __name__)


@opportunity.route('/add/', methods=['Get', 'POST'])
@login_required
def create_opportunity():
    #user_id = Opportunity.query.filter_by(user_id=current_user.id).filter_by(id=user_id).first_or_404()
    form = OpportunityForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            appt = Opportunity(title=form.title.data,
                       user_id=current_user.id,
                       city=form.city.data,
                       state=form._state.data,
                       country=form.country.data,
                       description=form.description.data,
                       #start_date=form.start_date.data.strftime('%d %B, %Y'),  # ''' ##('%Y-%m-%d') Alternative '''
                       #end_date=form.end_date.data.strftime('%d %B, %Y'),  # ''' ##('%Y-%m-%d') Alternative '''
                       title=form.title.data,
                       summary=form.summary.data,
                       opportunity_type=form.opportunity_type.data,
                       available_now=form.available_now.data,
                       location_type=form.location_type.data, 
                       )
            db.session.add(appt)
            db.session.commit()
            flash('Opportunity added!', 'success')
            return redirect(url_for('opportunity.opportunity_details', title=appt.title,
                                    city=appt.city, state=appt.state,
                                    country=appt.country))
        else:

            flash('ERROR! Opportunity was not added.', 'error')
    return render_template('opportunity/create_opportunity.html', form=form, opp=opp)

@opportunity.route('/list/')
def opportunity_list():
    #appts = opportunity.query.filter(opportunity.organisation != None).filter(opportunity.end_date >= datetime.now()).order_by(opportunity.pub_date.asc()).all()
    #return render_template('opportunity/allopportunity.html', appts=appts)
    #def opportunity_list():
    appts = Opportunity.query.all()
    return render_template('opportunity/allopportunities.html', appts=appts)




@opportunity.route('/<int:id>/<title>/<city>/<state>/<country>')
def opportunity_details(id, title, city, state, country):
    appts = Opportunity.query.filter(Opportunity.id == id).first_or_404()
    org_users = User.query.all()
    orgs = Opportunity.query.filter(Opportunity.user_id == User.id).all()
    return render_template('opportunity/opportunities_details.html', appt=appts, orgs=orgs, org_users=org_users)




##@opportunity.route('/<int:opportunity_id>/<opportunity_title>/apply')
##@login_required
##def opportunity_apply(opportunity_id, opportunity_title):
##    appt = db.session.query(opportunity).get(opportunity_id)
##    if appt is None:
##        abort(404)
##    elif current_user.id is None:
##        abort(403)
##    
##    else:
##        
##        if appt.creator == current_user:
##            flash("You can't apply to {0} because you created it".format(appt.opportunity_title), 'warning')
##            return redirect(url_for('opportunity.opportunity_list'))
##        extra = Extra.query.filter_by(user_id=current_user.id).first()
##        if not extra:
##            flash(
##                "You can't participate to {0} because you didn't add your extra details , please go to <a href='{1}'>profile</a> to add it".format(
##                    appt.opportunity_title, url_for('account.change_extra_details')), 'warning')
##            return redirect(url_for('opportunity.opportunity_list'))
##        submissions = Submission.query.filter(Submission.opportunity_id == appt.id).all()
##        submissions = [appt.user_id for appt in submissions]
##        if current_user.id in submissions:
##            flash("You have <strong>already participated</strong> for {0}.".format(appt.opportunity_title), 'warning')
##            return redirect(url_for('opportunity.opportunity_list'))
##        else:
##            appts = Submission(opportunity_id=appt.id, user_id=current_user.id)
##            db.session.add(appts)
##            db.session.commit()
##            flash("You have successfully participated to {0}.".format(appt.opportunity_title), 'success')
##            return redirect(url_for('opportunity.opportunity_list'))



