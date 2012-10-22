# -*- coding: utf-8 -*-

from . import db, BaseScopedIdNameMixin
from .workspace import WorkspaceForum


class Discussion(BaseScopedIdNameMixin, db.Model):
    __tablename__ = 'discussion'

    forum_id = db.Column(None, db.ForeignKey('workspace_forum.id'), nullable=False)
    forum = db.relationship(WorkspaceForum, backref=db.backref('discussions', cascade='all, delete-orphan'))
    parent = db.synonym('workspace')
    __table_args__ = (db.UniqueConstraint('url_id', 'forum_id'),)
