from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required
from app.models import EditableHTML, SiteSetting
from .forms import SiteSettingForm
import commonmark
from app import db
settings = Blueprint('settings', __name__)



@settings.route('/')
@login_required
def site_settings():
    all_settings = SiteSetting.query.all()
    return render_template("settings/index.html",
                           settings=all_settings)


@settings.route('/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_site_setting(id):
    form = SiteSettingForm()

    site_setting = SiteSetting.query.filter_by(id=id).first()

    if(site_setting is None):
        abort(404)

    if form.validate_on_submit():
        site_setting.value = form.value.data

        db.session.add(site_setting)
        flash('"{0}" has been saved'.format(site_setting.name))

        return redirect(url_for('.settings'))

    form.name.data = site_setting.name
    form.value.data = site_setting.value

    return render_template("settings/edit.html", form=form,
                           setting=site_setting)


@settings.route('/new', methods=['GET', 'POST'])
@login_required
def new_site_setting():
    form = SiteSettingForm()

    if form.validate_on_submit():
        site_setting = SiteSetting()
        site_setting.name = form.name.data
        site_setting.value = form.value.data

        db.session.add(site_setting)
        flash('"{0}" has been saved'.format(site_setting.name))

        return redirect(url_for('settings.site_settings'))

    return render_template("settings/new.html", form=form)


@settings.route('/delete/<int:id>')
@login_required
def delete_site_setting(id):
    setting = SiteSetting.query.filter_by(id=id).first()

    if(setting is not None):
        db.session.delete(setting)

        flash('"{0}" has been deleted.'.format(setting.name))
        return redirect(url_for('settings.site_settings'))

    flash('Setting does not exist')
    return redirect(url_for('settings.site_settings'))