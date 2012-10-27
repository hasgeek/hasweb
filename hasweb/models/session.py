# -*- coding: utf-8 -*-

from flask import url_for
from . import db, BaseScopedIdNameMixin
from hasweb.models.funnel import Proposal
from hasweb.models import commentease
from hasweb.models.user import User
from hasweb.models.venue import VenueRoom


__all__ = ['Proposal']


class SESSION_STATUS:
    CONFIRMED = 1
    TENTATIVE = 2
    CLOSED = 3

proposal_status = {
    1: u'CONFIRMED',
    2: u'TENTATIVE',
    3: u'CLOSED'
}


class Session(BaseScopedIdNameMixin):
    __tablename__ = 'session'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(User)
    parent = db.synonym('user')

    proposal_id = db.Column(None, db.ForeignKey('proposal.id'), nullable=False)
    proposal = db.relationship(Proposal)

    description = db.Column(db.UnicodeText, default=u"", nullable=False)
    description_format = db.Column(db.Unicode(20), default=u'html',
                                                         nullable=False)
    description_html = db.Column(db.UnicodeText, default=u"", nullable=False)

    venue_room_id = db.Column(None, db.ForeignKey('venue_room.id'),
                                                        nullable=False)
    venue_room = db.relationship(VenueRoom)

    start_datetime = db.Column(db.DateTime, nullable=False)
    end_datetime = db.Column(db.DateTime, nullable=False)
