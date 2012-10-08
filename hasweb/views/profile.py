# -*- coding: utf-8 -*-

from flask import render_template
from coaster.views import load_model
from hasweb import app
from hasweb.models import Profile


@app.route('/<profile>', endpoint='profile')
@load_model(Profile, {'name': 'profile'}, 'profile')
def profile_view(profile):
    return render_template('profile.html', profile=profile)
