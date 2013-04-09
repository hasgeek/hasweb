# -*- coding: utf-8 -*-

from flask import url_for
from flask.ext.lastuser.sqlalchemy import UserBase, TeamBase
from . import db
from .profile import Profile

__all__ = ['User', 'Team']


class User(UserBase, db.Model):
    @property
    def profile_url(self):
        return url_for('profile', profile=self.username or self.userid)

    @property
    def profile(self):
        return Profile.query.filter_by(userid=self.userid).first()

    @property
    def profiles(self):
        return [self.profile] + Profile.query.filter(
            Profile.userid.in_(self.organizations_owned_ids())).order_by('title').all()


class Team(TeamBase, db.Model):
    pass
