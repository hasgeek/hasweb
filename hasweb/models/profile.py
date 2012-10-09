# -*- coding: utf-8 -*-

from . import db, BaseNameMixin

__all__ = ['PROFILE_TYPE', 'Profile']


class PROFILE_TYPE:
    UNDEFINED = 0
    PERSON = 1
    ORGANIZATION = 2
    EVENTSERIES = 3
    COMMUNITY = 4

profile_types = {
    0: u"Undefined",
    1: u"Person",
    2: u"Organization",
    3: u"Event Series",
    4: u"Community",
    }


class Profile(BaseNameMixin, db.Model):
    __tablename__ = 'profile'

    userid = db.Column(db.Unicode(22), nullable=False, unique=True)
    description = db.Column(db.UnicodeText, default=u'', nullable=False)
    type = db.Column(db.Integer, default=PROFILE_TYPE.UNDEFINED, nullable=False)

    def type_label(self):
        return profile_types.get(self.type, profile_types[0])

    def permissions(self, user, inherited=None):
        perms = super(Profile, self).permissions(user, inherited)
        perms.add('view')
        if user.userid == self.userid:
            perms.add('edit')

        return perms
