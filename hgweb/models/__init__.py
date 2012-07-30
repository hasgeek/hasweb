# -*- coding: utf-8 -*-

from flask.ext.sqlalchemy import SQLAlchemy
from hgweb import app
from coaster.sqlalchemy import IdMixin, TimestampMixin, BaseMixin, BaseNameMixin

db = SQLAlchemy(app)

from hgweb.models.user import *
