# -*- coding: utf-8 -*-

from flask.ext.lastuser.sqlalchemy import UserBase
from hgweb.models import db

__all__ = ['User']


class User(db.Model, UserBase):
    __tablename__ = 'user'
