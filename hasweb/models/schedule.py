# -*- coding: utf-8 -*-

from . import db, BaseMixin
from .workspace import WorkspaceSchedule
from .user import User
from .funnel import Proposal
from datetime import datetime
from .venue import VenueCampus


__all__ = ['Schedule']


class Schedule(BaseMixin, db.Model):
    __tablename__ = 'schedule'

    workspace_schedule_id = db.Column(None, db.ForeignKey('workspace_schedule.id'), nullable=False)
    workspace_schedule = db.relationship(WorkspaceSchedule,
        backref=db.backref('session', cascade='all, delete-orphan'))
    parent = db.synonym('workspace_schedule')

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(User)
    parent = db.synonym('user')

    venue_campus_id = db.Column(None, db.ForeignKey('venue_campus.id'), nullable=False)
    venue_campus = db.relationship(VenueCampus)
    proposal_id = db.Column(None, db.ForeignKey('proposal.id'), nullable=False)
    proposal = db.relationship(Proposal,
        backref=db.backref('schdeule_proposals', cascade='all, delete-orphan'))
    start_datetime = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    end_datetime = db.Column(db.DateTime, default=datetime.utcnow,  nullable=False)
