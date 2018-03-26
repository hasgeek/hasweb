# -*- coding: utf-8 -*-

import os.path
from flask import render_template, redirect, url_for
from .. import app, pages


@app.route('/')
def index():
    return render_template('index.html.jinja2')


@app.route('/about/', defaults={'path': 'index'})
@app.route('/about/policy/', defaults={'path': 'policy/index'})
@app.route('/about/<path:path>')
def about(path):
    return render_template('about.html.jinja2', page=pages.get_or_404(os.path.join('about', path)))


# Deprecated: site policy pages have moved from /site to /about/policy
@app.route('/site/', defaults={'path': 'index'})
@app.route('/site/<path:path>')
def sitepolicy(path):
    return redirect(url_for('about', path='policy/' + path))
