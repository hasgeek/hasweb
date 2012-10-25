# -*- coding: utf-8 -*-

from flask import url_for
from . import db, BaseScopedIdNameMixin, VotingMixin, CommentingMixin
from hasweb.models.workspace import WorkspaceFunnel
from hasweb.models import commentease
from hasweb.models.user import User

__all__ = ['Proposal']


class PROPOSAL_STATUS:
    DRAFT = 1
    PUBLIC = 2
    PRIVATE = 3

proposal_status = {
    1: u'DRAFT',
    2: u'PUBLIC',
    3: u'PRIVATE'
}


class Proposal(BaseScopedIdNameMixin, VotingMixin, CommentingMixin, db.Model):
    __tablename__ = 'proposal'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(User)
    parent = db.synonym('user')

    workspace_funnel_id = db.Column(None, db.ForeignKey('workspace_funnel.id'), nullable=False)
    workspace_funnel = db.relationship(WorkspaceFunnel, backref=db.backref('proposals', cascade='all, delete-orphan'))
    parent = db.synonym('workspace_funnel')
    description = db.Column(db.UnicodeText, default=u"", nullable=False)
    description_format = db.Column(db.Unicode(20), default=u'html', nullable=False)
    description_html = db.Column(db.UnicodeText, default=u"", nullable=False)
    is_speaking = db.Column(db.Integer, default=True, nullable=False)
    confirmed = db.Column(db.Boolean, default=False, nullable=False)
    status = db.Column(db.Integer, default=PROPOSAL_STATUS.DRAFT, nullable=False)

    __table_args__ = (db.UniqueConstraint('url_id', "workspace_funnel_id"),)

    def __init__(self, **kwargs):
        super(Proposal, self).__init__(**kwargs)
        self.votes = commentease.VoteSpace()
        self.comments = commentease.CommentSpace()

    def permissions(self, user, inherited=None):
        perms = super(Proposal, self).permissions(user, inherited)
        perms.add('view')
        if user and self.user.userid in user.user_organizations_owned_ids():
            perms.add('edit')
            perms.add('delete')
            perms.add('new')
        return perms

    def url_for(self, action='view'):
        workspace = self.workspace_funnel.workspace
        if action == 'view':
            return url_for('funnel_view', profile=workspace.profile.name, workspace=workspace.name, proposal=self.url_name)
        elif action == 'edit':
            return url_for('funnel_edit', profile=workspace.profile.name, workspace=workspace.name, proposal=self.url_name)
        elif action == 'delete':
            return url_for('funnel_delete', profile=workspace.profile.name, workspace=workspace.name, proposal=self.url_name)
        elif action == 'action':
            return url_for('funnel_action', profile=workspace.profile.name, workspace=workspace.name, proposal=self.url_name)

        # Redo these:
        elif action == 'cancelsessionvote':
            return url_for('cancelsessionvote', profile=workspace.profile.name, workspace=workspace.name, proposal=self.url_name)
        elif action == 'voteupsession':
            return url_for('voteupsession', profile=workspace.profile.name, workspace=workspace.name, proposal=self.url_name)
        elif action == 'votedownsession':
            return url_for('votedownsession', profile=workspace.profile.name, workspace=workspace.name, proposal=self.url_name)
        elif action == 'confirm_session':
            return url_for('confirm_session', profile=workspace.profile.name, workspace=workspace.name, proposal=self.url_name)

    def __repr__(self):
        return u'<Proposal "%s" in workspace "%s" by "%s">' % (self.title, self.title, self.user.fullname)

    def getnext(self):
        return Proposal.query.filter(Proposal.workspace_funnel == self.workspace_funnel).filter(
            Proposal.id != Proposal.id).filter(
            Proposal.created_at < Proposal.created_at).order_by(db.desc('created_at')).first()

    def getprev(self):
        return Proposal.query.filter(Proposal.workspace_funnel == self.workspace_funnel).filter(
            Proposal.id != self.id).filter(
            Proposal.created_at > self.created_at).order_by('created_at').first()
