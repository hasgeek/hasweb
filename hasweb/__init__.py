# -*- coding: utf-8 -*-

from markdown import Markdown

# The imports in this file are order-sensitive

from flask import Flask
from flask.ext.flatpages import FlatPages
from flask.ext.lastuser import Lastuser
from flask.ext.lastuser.sqlalchemy import UserManager
from baseframe import baseframe, assets, Version
import coaster.app
from ._version import __version__


version = Version(__version__)
app = Flask(__name__, instance_relative_config=True)
lastuser = Lastuser()
pages = FlatPages()

assets['hasweb.css'][version] = 'css/app.css'

from . import models, views


@app.template_filter('markdown')
def to_markdown(text):
    markdown = Markdown(safe_mode="escape").convert
    return markdown(text)


def init_for(env):
    coaster.app.init_app(app, env)
    baseframe.init_app(app, requires=['baseframe', 'hasweb'])
    lastuser.init_app(app)
    lastuser.init_usermanager(UserManager(models.db, models.User, models.Team))
    pages.init_app(app)
