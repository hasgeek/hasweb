# -*- coding: utf-8 -*-

# The imports in this file are order-sensitive

from flask import Flask
from flask_flatpages import FlatPages
from flask_lastuser import Lastuser
from flask_lastuser.sqlalchemy import UserManager
from baseframe import baseframe, assets, Version
from flask_migrate import Migrate
import coaster.app
from ._version import __version__


version = Version(__version__)
app = Flask(__name__, instance_relative_config=True)
lastuser = Lastuser()
pages = FlatPages()

assets['hasweb.css'][version] = 'css/app.css'

from . import models, views  # NOQA

# Configure the app
coaster.app.init_app(app)
migrate = Migrate(app, models.db)
baseframe.init_app(app, requires=['baseframe-bs3', 'fontawesome', 'ractive', 'hasweb'])
lastuser.init_app(app)
lastuser.init_usermanager(UserManager(models.db, models.User))
pages.init_app(app)
