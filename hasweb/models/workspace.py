# -*- coding: utf-8 -*-

from flask import url_for
from . import db, BaseMixin, BaseScopedNameMixin, VotingMixin, CommentingMixin
from .profile import Profile
from hasweb.models import commentease


__all__ = ['Workspace', 'WorkspaceFunnel', 'WorkspaceSchedule']


class WORKSPACE:
    FUNNEL = 1
    SCHEDULE = 2
    FORUM = 4


workspace_types = {
    1: u"Funnel",
    2: u"Schedule",
    4: u"Forum"
}


class FUNNEL_STATUS:
    DRAFT = 0
    SUBMISSIONS = 1
    VOTING = 2
    JURY = 3
    FEEDBACK = 4
    CLOSED = 5
    REJECTED = 6


funnel_status = {
    0: u"Draft",
    1: u"Submissions",
    2: u"Voting",
    3: u"Jury",
    4: u"Feedback",
    5: u"Closed",
    6: u"Rejected"
}


class PROPOSAL_STATUS:
    DRAFT = 0
    SUBMISSIONS = 1
    VOTING = 2
    JURY = 3
    FEEDBACK = 4
    CLOSED = 5
    REJECTED = 6


proposal_status = {
    0: u"Draft",
    1: u"Submissions",
    2: u"Voting",
    3: u"Jury",
    4: u"Feedback",
    5: u"Closed",
    6: u"Rejected"
}


class SPACESTATUS:
    DRAFT = 0
    SUBMISSIONS = 1
    VOTING = 2
    JURY = 3
    FEEDBACK = 4
    CLOSED = 5
    REJECTED = 6


class COMMENTSTATUS:
    PUBLIC = 0
    SCREENED = 1
    HIDDEN = 2
    SPAM = 3
    DELETED = 4  # For when there are children to be preserved


# What is this VoteSpace or CommentSpace attached to?
class SPACETYPE:
    PROPOSALSPACE = 0
    PROPOSALSPACESECTION = 1
    PROPOSAL = 2
    COMMENT = 3


class Workspace(BaseScopedNameMixin, db.Model):
    __tablename__ = 'workspace'

    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)
    profile = db.relationship(Profile)
    parent = db.synonym('profile')

    description = db.Column(db.UnicodeText, default=u"", nullable=False)

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

    def url_for(self, action='view'):
        if action == 'view':
            return url_for('workspace', profile=self.profile.name, workspace=self.name)


class WorkspaceFunnel(BaseMixin, db.Model):
    __tablename__ = 'workspace_funnel'
    workspace_id = db.Column(None, db.ForeignKey('workspace.id'), nullable=False)
    workspace = db.relationship(Workspace, backref=db.backref('funnel', cascade='all, delete-orphan'))

    status = db.Column(db.Integer, default=FUNNEL_STATUS.DRAFT, nullable=False)
    proposal_template = db.Column(db.UnicodeText, default=u"", nullable=False)

    def __init__(self, **kwargs):
        super(WorkspaceFunnel, self).__init__(**kwargs)


class WorkspaceSchedule(BaseMixin, db.Model):
    __tablename__ = 'workspace_schedule'
    workspace_id = db.Column(None, db.ForeignKey('workspace.id'), nullable=False)
    workspace = db.relationship(Workspace, backref=db.backref('schedule', cascade='all, delete-orphan'))


class WorkspaceForum(BaseMixin, db.Model):
    __tablename__ = 'workspace_forum'
    workspace_id = db.Column(None, db.ForeignKey('workspace.id'), nullable=False)
    workspace = db.relationship(Workspace, backref=db.backref('forum', cascade='all, delete-orphan'))
