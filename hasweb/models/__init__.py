# -*- coding: utf-8 -*-

from flask.ext.sqlalchemy import SQLAlchemy
from coaster.sqlalchemy import IdMixin, TimestampMixin, BaseMixin, BaseNameMixin, BaseScopedNameMixin, BaseScopedIdNameMixin
from hasweb import app

__all__ = ['db']

db = SQLAlchemy(app)

from hasweb.models.user import *
from hasweb.models.profile import *
from hasweb.models.workspace import *
