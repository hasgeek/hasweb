# -*- coding: utf-8 -*-

from flask import render_template
from coaster.views import load_models
from hasweb import app
from hasweb.models import Profile, Workspace


@app.route('/<profile>/<workspace>', endpoint='workspace')
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Workspace, {'name': 'workspace', 'profile': 'profile'}, 'workspace')
    )
def workspace_view(profile, workspace):
    return render_template('workspace.html', profile=profile, workspace=workspace)
