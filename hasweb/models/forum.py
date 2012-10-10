# -*- coding: utf-8 -*-

from . import db, BaseScopedIdNameMixin
from .workspace import Workspace
from .profile import Profile


class Forum(BaseScopedIdNameMixin, db.Model):
    __tablename__ = 'forum'

    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)
    profile = db.relationship(Profile)
    parent = db.synonym('profile')

    workspace_id = db.Column(None, db.ForeignKey('workspace.id'), nullable=False)
    workspace = db.relationship(Workspace, backref=db.backref('proposals', cascade='all, delete-orphan'))
    parent = db.synonym('workspace')
    __table_args__ = (db.UniqueConstraint('name', 'workspace_id'),)
