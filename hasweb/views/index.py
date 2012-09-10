# -*- coding: utf-8 -*-

import os.path
from flask import render_template
from hasweb import app, pages
from hasweb.forms import ProfileImageForm
from hasweb.views.login import lastuser


lastuser.external_resource('imgee/list', 'http://0.0.0.0:4500/list', 'GET')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/profile/upload', methods=['GET', 'POST'])
@lastuser.requires_login
def upload_profile():
    foo = lastuser.call_resource(name='imgee/list')
    print foo
    form = ProfileImageForm(csrf=False)
    if form.validate_on_submit():
        pass
    return render_template('upload.html', form=form)



@app.route('/about/', defaults={'path': 'index'})
@app.route('/about/<path:path>')
def about(path):
    return render_template('about.html', page=pages.get_or_404(os.path.join('about', path)))


@app.route('/site/', defaults={'path': 'index'})
@app.route('/site/<path:path>')
def sitepolicy(path):
    return render_template('site.html', page=pages.get_or_404(os.path.join('site', path)))
