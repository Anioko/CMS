from flask import Blueprint, render_template, abort, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_required
from sqlalchemy.orm import lazyload

from app.models import *
from app.candidate.forms import *


candidate = Blueprint('candidate', __name__)


@candidate.route('/list/', defaults={'page': 1})
@candidate.route('/list/page/<int:page>', methods=['GET'])
@login_required
def select_section(page):
    paginated = User.query.filter(User.id != current_user.id).order_by(User.id.desc()).paginate(page, per_page=25)
    return render_template('candidate/selection.html', paginated=paginated)


@candidate.route('/test/')
def candidate_list():
    #appts = candidate.query.filter(candidate.organisation != None).filter(candidate.end_date >= datetime.now()).order_by(candidate.pub_date.asc()).all()
    #return render_template('candidate/allcandidate.html', appts=appts)
    #def candidate_list():
    appts = User.query.all()
    # same, using class-bound attribute
    appt = db.session.query(User).options(lazyload(User.schools)).all()
    return render_template('candidate/index.html', appts=appts, appt=appt)




@candidate.route('/<int:id>/<title>/<city>/<state>/<country>')
def candidate_details(id, title, city, state, country):
    appts = Candidate.query.filter(Candidate.id == id).first_or_404()
    org_users = User.query.all()
    orgs = Candidate.query.filter(Candidate.user_id == User.id).all()
    return render_template('candidate/opportunities_details.html', appt=appts, orgs=orgs, org_users=org_users)




##@candidate.route('/<int:candidate_id>/<candidate_title>/apply')
##@login_required
##def candidate_apply(candidate_id, candidate_title):
##    appt = db.session.query(candidate).get(candidate_id)
##    if appt is None:
##        abort(404)
##    elif current_user.id is None:
##        abort(403)
##    
##    else:
##        
##        if appt.creator == current_user:
##            flash("You can't apply to {0} because you created it".format(appt.candidate_title), 'warning')
##            return redirect(url_for('candidate.candidate_list'))
##        extra = Extra.query.filter_by(user_id=current_user.id).first()
##        if not extra:
##            flash(
##                "You can't participate to {0} because you didn't add your extra details , please go to <a href='{1}'>profile</a> to add it".format(
##                    appt.candidate_title, url_for('account.change_extra_details')), 'warning')
##            return redirect(url_for('candidate.candidate_list'))
##        submissions = Submission.query.filter(Submission.candidate_id == appt.id).all()
##        submissions = [appt.user_id for appt in submissions]
##        if current_user.id in submissions:
##            flash("You have <strong>already participated</strong> for {0}.".format(appt.candidate_title), 'warning')
##            return redirect(url_for('candidate.candidate_list'))
##        else:
##            appts = Submission(candidate_id=appt.id, user_id=current_user.id)
##            db.session.add(appts)
##            db.session.commit()
##            flash("You have successfully participated to {0}.".format(appt.candidate_title), 'success')
##            return redirect(url_for('candidate.candidate_list'))



