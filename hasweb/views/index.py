# -*- coding: utf-8 -*-

import os.path
from werkzeug import secure_filename
from flask import render_template, g, request
from hasweb import app, pages
from hasweb.forms import ProfileImageForm
from hasweb.views.login import lastuser


lastuser.external_resource('imgee/list', 'http://0.0.0.0:4500/list', 'GET')
lastuser.external_resource('imgee/upload', 'http://0.0.0.0:4500/upload', 'POST')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/profile/upload', methods=['GET', 'POST'])
@lastuser.requires_login
def upload_profile():
    form = ProfileImageForm(csrf=False)
    if request.method == 'POST':
        imagefile = request.files['image_file']
        if imagefile:
            filename = secure_filename(imagefile.filename)
            imagefile.save(os.path.join('hasweb/static/upload', filename))
            with open(os.path.join('hasweb/static/upload', filename), 'r') as uploadedfile:
                foo = lastuser.call_resource(name='imgee/upload', profileid=g.user.userid, files={'stored_file':uploadedfile})
                print foo
    return render_template('upload.html', form=form)



@app.route('/about/', defaults={'path': 'index'})
@app.route('/about/<path:path>')
def about(path):
    return render_template('about.html', page=pages.get_or_404(os.path.join('about', path)))


@app.route('/site/', defaults={'path': 'index'})
@app.route('/site/<path:path>')
def sitepolicy(path):
    return render_template('site.html', page=pages.get_or_404(os.path.join('site', path)))
