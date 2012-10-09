# -*- coding: utf-8 -*-

from . import db, BaseMixin, BaseScopedNameMixin

__all__ = ['Workspace']


class WORKSPACE:
    FUNNEL = 1
    SCHEDULE = 2
    FORUM = 4


class Workspace(BaseScopedNameMixin, db.Model):
    __tablename__ = 'workspace'

    feature_flags = db.Column(db.Integer, default=0, nullable=False)

    @property
    def has_funnel(self):
        return True if self.feature_flags & WORKSPACE.FUNNEL else False

    @property
    def has_schedule(self):
        return True if self.feature_flags & WORKSPACE.SCHEDULE else False

    @property
    def has_forum(self):
        return True if self.feature_flags & WORKSPACE.FORUM else False

    def enable_funnel(self):
        if not self.funnel:
            self.funnel = WorkspaceFunnel(workspace=self)
            db.session.add(self.funnel)
        self.feature_flags |= WORKSPACE.FUNNEL

    def disable_funnel(self):
        if self.funnel:
            db.session.delete(self.funnel)
        self.funnel = None
        self.feature_flags &= ~WORKSPACE.FUNNEL

    def enable_schedule(self):
        if not self.schedule:
            self.schedule = WorkspaceSchedule(workspace=self)
            db.session.add(self.schedule)
        self.feature_flags |= WORKSPACE.SCHEDULE

    def disable_schedule(self):
        if self.schedule:
            db.session.delete(self.schedule)
        self.schedule = None
        self.feature_flags &= ~WORKSPACE.SCHEDULE

    def enable_forum(self):
        if not self.forum:
            self.forum = WorkspaceForum(workspace=self)
            db.session.add(self.forum)
        self.feature_flags |= ~WORKSPACE.FORUM

    def disable_forum(self):
        if self.forum:
            db.session.delete(self.forum)
        self.forum = None
        self.feature_flags &= ~WORKSPACE.FORUM

    def permissions(self, user, inherited=None):
        perms = super(Workspace, self).permissions(user, inherited)
        return perms


class WorkspaceFunnel(BaseMixin, db.Model):
    __tablename__ = 'workspace_funnel'
    workspace_id = db.Column(None, db.ForeignKey('workspace.id'), nullable=False)
    workspace = db.relationship(Workspace, backref=db.backref('funnel', cascade='all, delete-orphan'))


class WorkspaceSchedule(BaseMixin, db.Model):
    __tablename__ = 'workspace_schedule'
    workspace_id = db.Column(None, db.ForeignKey('workspace.id'), nullable=False)
    workspace = db.relationship(Workspace, backref=db.backref('schedule', cascade='all, delete-orphan'))


class WorkspaceForum(BaseMixin, db.Model):
    __tablename__ = 'workspace_forum'
    workspace_id = db.Column(None, db.ForeignKey('workspace.id'), nullable=False)
    workspace = db.relationship(Workspace, backref=db.backref('forum', cascade='all, delete-orphan'))
