# -*- coding: utf-8 -*-

from flask import url_for
from flask.ext.lastuser.sqlalchemy import UserBase
from . import db

__all__ = ['User']


class User(db.Model, UserBase):
    __tablename__ = 'user'

    @property
    def profile_url(self):
        return url_for('profile', profile=self.username or self.userid)
