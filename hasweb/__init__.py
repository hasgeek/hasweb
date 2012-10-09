# -*- coding: utf-8 -*-

# The imports in this file are order-sensitive

from flask import Flask
from flask.ext.assets import Environment, Bundle
from flask.ext.flatpages import FlatPages
from flask.ext.lastuser import Lastuser
from flask.ext.lastuser.sqlalchemy import UserManager
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
js = Bundle(baseframe_js)
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
