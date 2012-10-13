# -*- coding: utf-8 -*-

from . import db, BaseNameMixin

__all__ = ['VenueRoom', 'VenueCampus']


class VenueCampus(BaseNameMixin, db.Model):
    __tablename__ = 'venue_campus'
    description = db.Column(db.UnicodeText, default=u'', nullable=False)
    address1 = db.Column(db.Unicode(80), default=u'', nullable=False)
    address2 = db.Column(db.Unicode(80), default=u'', nullable=False)
    postcode = db.Column(db.Unicode(10), default=u'', nullable=False)
    geonameid = db.Column(db.Integer, nullable=False)
    latitude = db.Column(db.Numeric(8, 5), nullable=True)
    longitude = db.Column(db.Numeric(8, 5), nullable=True)


class VenueRoom(BaseNameMixin, db.Model):
    __tablename__ = 'venue_room'
    description = db.Column(db.UnicodeText, default=u'', nullable=False)
    campus_id = db.Column(None, db.ForeignKey('venue_campus.id'), nullable=False)
    campus = db.relationship(VenueCampus, backref=db.backref('rooms', cascade='all, delete-orphan'))
    latitude = db.Column(db.Numeric(8, 5), nullable=True)
    longitude = db.Column(db.Numeric(8, 5), nullable=True)
