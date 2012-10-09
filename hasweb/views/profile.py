# -*- coding: utf-8 -*-

from flask import render_template
from coaster.views import load_model

from hasweb import app, lastuser
from hasweb.models import Profile
from hasweb.forms import ProfileForm


@app.route('/<profile>', endpoint='profile')
@load_model(Profile, {'name': 'profile'}, 'profile', permission='view')
def profile_view(profile):
    return render_template('profile.html', profile=profile)


@app.route('/<profile>/edit', methods=['GET', 'POST'])
@lastuser.requires_login
@load_model(Profile, {'name': 'profile'}, 'profile', permission='edit')
def profile_edit(profile):
    # TODO: Return edit form
    form = ProfileForm()
    return render_template('profile.html', profile=profile, form=form)
