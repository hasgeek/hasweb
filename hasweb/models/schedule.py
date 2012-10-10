# -*- coding: utf-8 -*-

from . import db, BaseMixin
from .workspace import WorkspaceSchedule, WorkspaceFunnel
from datetime import datetime
from .venue import VenueCampus


__all__ = ['Schedule']


class Schedule(BaseMixin, db.Model):
    __tablename__ = 'schedule'

    workspace_schedule_id = db.Column(None, db.ForeignKey('workspace_schedule.id'), nullable=False)
    workspace_schedule = db.relationship(WorkspaceSchedule,
        backref=db.backref('proposals', cascade='all, delete-orphan'))
    parent = db.synonym('workspace_schedule')
    venue_campus_id = db.Column(None, db.ForeignKey('venue_campus.id'), nullable=False)
    venue_campus = db.relationship(VenueCampus)
    workspace_funnel_id = db.Column(None, db.ForeignKey('workspace_funnel.id'), nullable=False)
    workspace_funnel = db.relationship(WorkspaceSchedule,
        backref=db.backref('workspace_funnels', cascade='all, delete-orphan'))
    start_datetime = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    end_datetime = db.Column(db.DateTime, default=datetime.utcnow,  nullable=False)
