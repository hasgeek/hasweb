# -*- coding: utf-8 -*-


from flask import url_for

from . import db, BaseNameMixin
from .user import User


__all__ = ['VenueRoom', 'VenueCampus']


class VenueCampus(BaseNameMixin, db.Model):
    __tablename__ = 'venue_campus'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(User)
    parent = db.synonym('user')

    description = db.Column(db.UnicodeText, default=u'', nullable=False)
    address1 = db.Column(db.Unicode(80), default=u'', nullable=False)
    address2 = db.Column(db.Unicode(80), default=u'', nullable=False)
    postcode = db.Column(db.Unicode(10), default=u'', nullable=False)
    geonameid = db.Column(db.Integer, nullable=False)
    latitude = db.Column(db.Numeric(8, 5), nullable=True)
    longitude = db.Column(db.Numeric(8, 5), nullable=True)

    def url_for(self, action='view'):
        if action == 'view':
            return url_for('venue_view', venue=self.name)
        elif action == 'edit':
            return url_for('venue_edit', venue=self.name)
        elif action == 'delete':
            return url_for('venue_delete', venue=self.name)

    def permissions(self, user, inherited=None):
        perms = super(VenueCampus, self).permissions(user, inherited)
        perms.add('view')
        if user and self.user.userid in user.user_organizations_owned_ids():
            perms.add('edit')
            perms.add('delete')
            perms.add('new')
        else:
            if 'edit' in perms:
                perms.remove('edit')
            if 'delete' in perms:
                perms.remove('delete')
        return perms

    @property
    def rooms(self):
        return VenueCampus.query.filter_by(venue=self).all()


class VenueRoom(BaseNameMixin, db.Model):
    __tablename__ = 'venue_room'
    description = db.Column(db.UnicodeText, default=u'', nullable=False)
    campus_id = db.Column(None, db.ForeignKey('venue_campus.id'), nullable=False)
    campus = db.relationship(VenueCampus, backref=db.backref('rooms', cascade='all, delete-orphan'))
    latitude = db.Column(db.Numeric(8, 5), nullable=True)
    longitude = db.Column(db.Numeric(8, 5), nullable=True)

    def url_for(self, action='edit'):
        if action == 'edit':
            return url_for('venue_campus_edit', venue=self.campus.name, room=self.name)
        elif action == 'delete':
            return url_for('venue_campus_delete', venue=self.campus.name, room=self.name)
