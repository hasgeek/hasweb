# -*- coding: utf-8 -*-

import os.path
from flask import render_template
from .. import app, pages


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about/', defaults={'path': 'index'})
@app.route('/about/<path:path>')
def about(path):
    return render_template('about.html', page=pages.get_or_404(os.path.join('about', path)))


@app.route('/site/', defaults={'path': 'index'})
@app.route('/site/<path:path>')
def sitepolicy(path):
    return render_template('about.html', page=pages.get_or_404(os.path.join('site', path)))
