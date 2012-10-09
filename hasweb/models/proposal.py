# -*- coding: utf-8 -*-

from . import db, BaseScopedIdNameMixin
from .workspace import Workspace


class Proposal(BaseScopedIdNameMixin, db.Model):
    __tablename__ = 'proposal'

    workspace_id = db.Column(None, db.ForeignKey('workspace.id'), nullable=False)
    workspace = db.relationship(Workspace, backref=db.backref('proposals', cascade='all, delete-orphan'))
    parent = db.synonym('workspace')
    __table_args__ = (db.UniqueConstraint('name', 'workspace_id'),)
