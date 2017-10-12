# -*- coding: utf-8 -*-

import os.path
from flask import render_template, redirect, url_for
from .. import app, pages


@app.route('/')
def index():
    return render_template('index.html.jinja2')


@app.route('/about/', defaults={'path': 'index'})
@app.route('/about/<path:path>')
def about(path):
    return render_template('about.html.jinja2', page=pages.get_or_404(os.path.join('about', path)))


@app.route('/about/policy/')
def about_policy():
    return about('policy/index')


@app.route('/about/policy/index')
def about_policy_index():
    return redirect(url_for('about_policy'))


@app.route('/site/', defaults={'path': 'index'})
@app.route('/site/<path:path>')
def sitepolicy(path):
    return redirect(url_for('about', path='policy/' + path))
