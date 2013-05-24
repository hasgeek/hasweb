# -*- coding: utf-8 -*-

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.commentease import Commentease, VotingMixin, CommentingMixin
from coaster.sqlalchemy import (IdMixin, TimestampMixin, BaseMixin, BaseNameMixin,
    BaseScopedNameMixin, BaseScopedIdNameMixin, make_name)
from hasweb import app

db = SQLAlchemy(app)
commentease = Commentease(db=db)

from .user import *
from .profile import *
from .venue import *
