# -*- coding: utf-8 -*-

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.commentease import Commentease, VotingMixin, CommentingMixin
from coaster.sqlalchemy import (IdMixin, TimestampMixin, BaseMixin, BaseNameMixin,
    BaseScopedNameMixin, BaseScopedIdNameMixin, make_name)
from hasweb import app

__all__ = ['db']

db = SQLAlchemy(app)

#Make votes, comments using Commentease

commentease = Commentease()
commentease.init_db(db)

from hasweb.models.user import *
from hasweb.models.profile import *
from hasweb.models.workspace import *
from hasweb.models.funnel import *
from hasweb.models.forum import *
from hasweb.models.venue import *
from hasweb.models.schedule import *
from hasweb.models.venue import *
