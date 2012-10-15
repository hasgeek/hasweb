# -*- coding: utf-8 -*-

from flask import url_for

from . import db, Profile, BaseNameMixin

__all__ = ['Venue', 'VenueCampus']


class Venue(BaseNameMixin, db.Model):
    __tablename__ = 'venue'
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=False)
    profile = db.relationship(Profile)
    description = db.Column(db.UnicodeText, default=u'', nullable=False)
    address1 = db.Column(db.Unicode(80), default=u'', nullable=False)
    address2 = db.Column(db.Unicode(80), default=u'', nullable=False)
    city = db.Column(db.Unicode(30), default=u'', nullable=False)
    state = db.Column(db.Unicode(30), default=u'', nullable=False)
    postcode = db.Column(db.Unicode(20), default=u'', nullable=False)
    country = db.Column(db.Unicode(2), default=u'', nullable=False)
    latitude = db.Column(db.Numeric(8, 5), nullable=True)
    longitude = db.Column(db.Numeric(8, 5), nullable=True)

    def url_for(self, action='view'):
        if action == 'view':
            return url_for('venue_view', venue=self.name)
        elif action == 'edit':
            return url_for('venue_edit', venue=self.name)
        elif action == 'delete':
            return url_for('venue_delete', venue=self.name)

    @property
    def rooms(self):
        return VenueCampus.query.filter_by(venue=self).all()


class VenueCampus(BaseNameMixin, db.Model):
    __tablename__ = 'venue_campus'

    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    description = db.Column(db.UnicodeText, default=u'', nullable=False)
    venue = db.relationship(Venue)

    def url_for(self, action='edit'):
        if action == 'edit':
            return url_for('venue_campus_edit', venue=self.venue.name, room=self.name)
        elif action == 'delete':
            return url_for('venue_campus_delete', venue=self.venue.name, room=self.name)
