# -*- coding: utf-8 -*-

from . import db, BaseMixin
from .schedule import Schedule

__all__ = ['FeedBack']


class FEEDBACK_RATING:
    OK = 0
    SAD = -1
    HAPPY = 1

feebback_ratings = {
    0: u"Ok",
    1: u"Happy",
    -1: u"Sad"
}


class FeedBack(BaseMixin, db.model):
    __tablename__ = u"feedback"

    schedule_id = db.Column(None, db.ForeignKey('schedule.id'), nullable=False)
    workspace_schedule = db.relationship(Schedule,
        backref=db.backref('schedules', cascade='all, delete-orphan'))
    rating = db.Column(db.Integer, default=FEEDBACK_RATING.OK, nullable=False)
