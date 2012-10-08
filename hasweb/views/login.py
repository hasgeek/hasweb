# -*- coding: utf-8 -*-

from flask import g, Response, redirect, flash
from coaster.views import get_next_url

from hasweb import app, lastuser
from hasweb.models import db, Profile, PROFILE_TYPE


@app.route('/login')
@lastuser.login_handler
def login():
    return {'scope': 'id email organizations'}


@app.route('/logout')
@lastuser.logout_handler
def logout():
    flash(u"You are now logged out", category='info')
    return get_next_url()


@app.route('/login/redirect')
@lastuser.auth_handler
def lastuserauth():
    if g.user:
        make_profiles_at_login(g.user)
        db.session.commit()
    return redirect(get_next_url())


@lastuser.auth_error_handler
def lastuser_error(error, error_description=None, error_uri=None):
    if error == 'access_denied':
        flash("You denied the request to login", category='error')
        return redirect(get_next_url())
    return Response(u"Error: %s\n"
                    u"Description: %s\n"
                    u"URI: %s" % (error, error_description, error_uri),
                    mimetype="text/plain")


def make_profiles_at_login(user):
    username = user.username or user.userid
    profile = Profile.query.filter_by(userid=user.userid).first()
    if profile is None:
        profile = Profile(userid=user.userid,
            name=user.username or user.userid,
            title=user.fullname,
            type=PROFILE_TYPE.PERSON)
        db.session.add(profile)
    else:
        if profile.name != username:
            profile.name = username
        if profile.title != user.fullname:
            profile.title = user.fullname
    for org in user.organizations_owned():
        profile = Profile.query.filter_by(userid=org['userid']).first()
        if profile is None:
            profile = Profile(userid=org['userid'],
                name=org['name'],
                title=org['title'],
                type=PROFILE_TYPE.ORGANIZATION)
            db.session.add(profile)
        else:
            if profile.name != org['name']:
                profile.name = org['name']
            if profile.title != org['title']:
                profile.title = org['title']
