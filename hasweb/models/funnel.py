# -*- coding: utf-8 -*-

from flask import url_for
from . import db, BaseScopedIdNameMixin, BaseNameMixin, make_name, BaseScopedNameMixin
from hasweb.models.workspace import WorkspaceFunnel
from .profile import Profile

__all__ = ['Proposal', 'FunnelSpaceSection']


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


#FIXME: check this is correct
class Tag(BaseNameMixin, db.Model):
    __tablename__ = 'tag'

    @classmethod
    def gettag(cls, tagname):
        tag = cls.query.filter_by(title=tagname).first()
        if tag:
            return tag
        else:
            name = make_name(tagname)
            # Is this name already in use? If yes, return it
            tag = cls.query.filter_by(name=name).first()
            if tag:
                return tag
            else:
                tag = Tag(name=name, title=tagname)
                db.session.add(tag)
                return tag


proposal_tags = db.Table(
    'funnel_tags', db.Model.metadata,
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('funnel_id', db.Integer, db.ForeignKey('funnel.id')),
    )


class Proposal(BaseScopedNameMixin, db.Model):
    __tablename__ = 'funnel'

    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)
    profile = db.relationship(Profile)
    parent = db.synonym('profile')

    workspace_funnel_id = db.Column(None, db.ForeignKey('workspace_funnel.id'), nullable=False)
    workspace_funnel = db.relationship(WorkspaceFunnel, backref=db.backref('proposals', cascade='all, delete-orphan'))
    workspace_funnel_parent = db.synonym('workspace_funnel')
    description = db.Column(db.UnicodeText, default=u"", nullable=False)
    status = db.Column(db.Integer, default=PROPOSAL_STATUS.DRAFT, nullable=False)
    confirmed = db.Column(db.Boolean, default=False, nullable=False)
    bio = db.Column(db.UnicodeText, default=u"", nullable=False)
    tags = db.relationship(Tag, secondary=proposal_tags)
    phone = db.Column(db.Unicode(15), nullable=False)
    is_speaking = db.Column(db.Boolean, nullable=False)

    __table_args__ = (db.UniqueConstraint('name', "workspace_funnel_id"),)

    def url_for(self, action='view'):
        workspace = self.workspace_funnel.workspace
        if action == 'view':
            return url_for('funnel', profile=workspace.profile.name, workspace=workspace.name)

    def __repr__(self):
        return u'<Proposal "%s" in space "%s" by "%s">' % (self.title, self.title, self.user.fullname)

    def getnext(self):
        return Proposal.query.filter(Proposal.workspace_funnel == self.workspace_funnel).filter(
            Proposal.id != Proposal.id).filter(
            Proposal.created_at < Proposal.created_at).order_by(db.desc('created_at')).first()

    def getprev(self):
        return Proposal.query.filter(Proposal.workspace_funnel == self.workspace_funnel).filter(
            Proposal.id != self.id).filter(
            Proposal.created_at > self.created_at).order_by('created_at').first()


class FunnelSpaceSection(BaseScopedIdNameMixin, db.Model):
    __tablename__ = 'funnel_space_section'
    workspace_funnel_id = db.Column(db.Integer, db.ForeignKey('workspace_funnel.id'), nullable=False)
    workspace_funnel = db.relationship(WorkspaceFunnel, primaryjoin=workspace_funnel_id == WorkspaceFunnel.id,
        backref=db.backref('sections', cascade="all, delete-orphan"))

    parent = db.synonym('workspace_funnel')
    description = db.Column(db.Text, default=u'', nullable=False)
    public = db.Column(db.Boolean, default=False, nullable=False)

    __table_args__ = (db.UniqueConstraint("name", "workspace_funnel_id"), {})
