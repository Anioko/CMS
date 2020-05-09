from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required
from app.models import EditableHTML, SiteSetting
from .forms import SiteSettingForm, PostForm, CategoryForm, EditCategoryForm
import commonmark
from app import db
from app.decorators import admin_required
from app.models import BlogPost
from app.models import BlogCategory
#from .forms import PostForm, CategoryForm, EditCategoryForm
settings = Blueprint('settings', __name__)



@settings.route('/')
@login_required
@admin_required
def site_settings():
    all_settings = SiteSetting.query.all()
    return render_template("settings/index.html",
                           settings=all_settings)


@settings.route('/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_site_setting(id):
    form = SiteSettingForm()

    site_setting = SiteSetting.query.filter_by(id=id).first()

    if(site_setting is None):
        abort(404)

    if form.validate_on_submit():
        site_setting.value = form.value.data

        db.session.add(site_setting)
        flash('"{0}" has been saved'.format(site_setting.name))

        return redirect(url_for('settings.site_settings'))

    form.name.data = site_setting.name
    form.value.data = site_setting.value

    return render_template("settings/edit.html", form=form,
                           setting=site_setting)


@settings.route('/new', methods=['GET', 'POST'])
@login_required
@admin_required
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
@admin_required
def delete_site_setting(id):
    setting = SiteSetting.query.filter_by(id=id).first()

    if(setting is not None):
        db.session.delete(setting)

        flash('"{0}" has been deleted.'.format(setting.name))
        return redirect(url_for('settings.site_settings'))

    flash('Setting does not exist')
    return redirect(url_for('settings.site_settings'))
    
@settings.route('/posts', defaults={'page': 1})
@settings.route('/posts/<int:page>')
@login_required
def blog_posts(page):
    the_posts = BlogPost.query.order_by(
        BlogPost.published_on.desc()).paginate(page, 5)
    return render_template('blog/posts/posts.html', js='posts/index', posts=the_posts)


@settings.route('/posts/<post_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_blog_post(post_id):
    form = PostForm()
    post = BlogPost.query.filter_by(id=post_id).first()

    if post is None:
        abort(404)

    if form.validate_on_submit():
        post.slug = form.slug.data
        post.title = form.title.data
        post.content = form.content.data
        post.published_on = form.published_on.data
        post.blogcategory_id = form.category.data
        post.blogpoststatus_id = form.status.data

        db.session.add(post)
        flash('"{0}" has been saved'.format(post.title))

        return redirect(url_for('.blog_posts'))

    form.slug.data = post.slug
    form.title.data = post.title
    form.content.data = post.content
    form.published_on.data = post.published_on
    form.category.data = post.blogcategory_id
    form.status.data = post.blogpoststatus_id

    return render_template('blog/posts/edit_post.html', js='posts/edit_post', form=form, post=post)


@settings.route('/posts/new', methods=['GET', 'POST'])
@login_required
@admin_required
def add_blog_post():
    form = PostForm()

    if form.validate_on_submit():
        post = BlogPost()

        post.slug = form.slug.data
        post.title = form.title.data
        post.content = form.content.data
        post.published_on = form.published_on.data
        post.user_id = current_user.id
        post.created_on = datetime.utcnow()
        post.blogcategory_id = form.category.data
        post.blogpoststatus_id = form.status.data

        db.session.add(post)
        flash('"{0}" has been saved'.format(post.title))

        return redirect(url_for('settings.blog_posts'))

    return render_template('blog/posts/add_post.html', js='posts/add_post', form=form)


@settings.route('/posts/delete/<post_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_blog_post(post_id):
    post = BlogPost.query.filter_by(id=post_id).first()

    if post is not None:
        db.session.delete(post)

        flash('"{0}" has been deleted.'.format(post.title))
        return redirect(url_for('.blog_posts'))

    flash('Post does not exist')
    return redirect(url_for('settings.blog_posts'))


@settings.route('/categories', defaults={'page': 1})
@settings.route('/categories/<int:page>')
@login_required
@admin_required
def blog_categories(page):
    the_categories = BlogCategory.query.order_by(
        BlogCategory.name).paginate(page, 5)
    return render_template('blog/categories/categories.html', categories=the_categories)


@settings.route('/categories/<int:category_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_blog_category(category_id):
    form = EditCategoryForm()
    category = BlogCategory.query.filter_by(id=category_id).first()

    if category is None:
        abort(404)

    if form.validate_on_submit():
        category.name = form.name.data
        category.slug = form.slug.data
        category.description = form.description.data

        db.session.add(category)
        flash('"{0}" has been saved'.format(category.name))

        return redirect(url_for('settings.blog_categories'))

    form.name.data = category.name
    form.slug.data = category.slug
    form.description.data = category.description

    return render_template('blog/categories/edit_category.html',
                           js='posts/add_edit_category', form=form,
                           category=category)


@settings.route('/categories/new', methods=['GET', 'POST'])
@login_required
@admin_required
def add_blog_category():
    form = EditCategoryForm()

    if form.validate_on_submit():
        category = BlogCategory()

        category.name = form.name.data
        category.slug = form.slug.data
        category.description = form.description.data
        category.created_on = datetime.utcnow()

        db.session.add(category)
        flash('"{0}" has been saved'.format(category.name))

        return redirect(url_for('settings.blog_categories'))

    return render_template('blog/categories/add_category.html', js='posts/add_edit_category', form=form)


@settings.route('/categories/delete/<int:category_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_blog_category(category_id):
    category = BlogCategory.query.filter_by(id=category_id).first()

    if category is not None:
        db.session.delete(category)

        flash('"{0}" has been deleted'.format(category.name))
        return redirect(url_for('settings.blog_categories'))

    flash('Category does not exist')
    return redirect('settings.blog_categories')