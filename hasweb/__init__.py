# -*- coding: utf-8 -*-

from markdown import Markdown

# The imports in this file are order-sensitive

from flask import Flask
from flask.ext.assets import Environment, Bundle
from flask.ext.flatpages import FlatPages
from flask.ext.lastuser import Lastuser
from flask.ext.lastuser.sqlalchemy import UserManager

from datetime import datetime

from baseframe import baseframe, baseframe_js, baseframe_css
import coaster.app

# First, make an app and config it

app = Flask(__name__, instance_relative_config=True)
lastuser = Lastuser()
pages = FlatPages(app)

# Second, after config, import the models and views

import hasweb.models
import hasweb.views

# Third, setup baseframe and assets

app.register_blueprint(baseframe)

assets = Environment(app)
js = Bundle(baseframe_js,
        'js/script.js',
        'js/jquery.tablesorter.min.js',
        'js/jquery.textarea-expander.js',
        'js/showdown.js')
css = Bundle(baseframe_css,
             'css/app.css',
             filters='cssmin', output='css/packed.css')
assets.register('js_all', js)
assets.register('css_all', css)


def init_for(env):
    coaster.app.init_app(app, env)
    hasweb.models.db.init_app(app)
    lastuser.init_app(app)
    lastuser.init_usermanager(UserManager(hasweb.models.db, hasweb.models.User))


@app.template_filter('age')
def age(dt):
    suffix = u"ago"
    delta = datetime.utcnow() - dt
    if delta.days == 0:
        # < 1 day
        if delta.seconds < 10:
            return "seconds %s" % suffix
        elif delta.seconds < 60:
            return "%d seconds %s" % (delta.seconds, suffix)
        elif delta.seconds < 120:
            return "a minute %s" % suffix
        elif delta.seconds < 3600:  # < 1 hour
            return "%d minutes %s" % (int(delta.seconds / 60), suffix)
        elif delta.seconds < 7200:  # < 2 hours
            return "an hour %s" % suffix
        else:
            return "%d hours %s" % (int(delta.seconds / 3600), suffix)
    elif delta.days == 1:
        return u"a day %s" % suffix
    else:
        return u"%d days %s" % (delta.days, suffix)


@app.template_filter('markdown')
def to_markdown(text):
    markdown = Markdown(safe_mode="escape").convert
    return markdown(text)
