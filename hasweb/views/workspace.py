# -*- coding: utf-8 -*-

from flask import render_template, abort, flash
from coaster.views import load_models, load_model
from baseframe.forms import render_form, render_redirect
from hasweb import app
from hasweb.models import Profile, db
from hasweb.views.login import lastuser
from hasweb.models.workspace import Workspace, WORKSPACE, WorkspaceFunnel
from hasweb.models.profile import PROFILE_TYPE
from hasweb.forms.workspace import FunnelSpaceForm


@app.route('/<profile>/<workspace>', endpoint='workspace')
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Workspace, {'name': 'workspace', 'profile': 'profile'}, 'workspace')
    )
def workspace_view(profile, workspace):
    return render_template('workspace.html', profile=profile, workspace=workspace)


@app.route('/<profile>/new', methods=['POST', 'GET'])
@lastuser.requires_login
@load_model(Profile, {'name': 'profile'}, 'profile', permission='new')
def funnel_new(profile):
    form = FunnelSpaceForm()
    if profile.type != PROFILE_TYPE.ORGANIZATION:
        abort(403)
    if form.validate_on_submit():
        workspace = Workspace(profile=profile)
        workspace_funnel = WorkspaceFunnel(workspace=workspace)
        form.populate_obj(workspace)
        if not workspace.name:
            workspace.make_name()
        workspace_funnel.status = workspace.status
        workspace_funnel.proposal_template = workspace.proposal_template
        workspace.feature_flags = WORKSPACE.FUNNEL
        db.session.add(workspace)
        db.session.add(workspace_funnel)
        db.session.commit()
        flash(u"Created Event '%s'" % workspace.title, 'success')
        return render_redirect(workspace.url_for(), code=303)
    return render_form(form=form, title="New Workspace - Event", submit=u"Save",
        cancel_url=profile.url_for(), ajax=True)


@app.route('/<profile>/<workspace>/edit', methods=['POST', 'GET'])
@lastuser.requires_login
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Workspace, {'name': 'workspace', 'profile': 'profile'}, 'workspace'),
permission='edit')
def funnel_edit(profile, workspace):
    if profile.type != PROFILE_TYPE.ORGANIZATION:
        abort(403)
    form = FunnelSpaceForm(obj=workspace)
    workspace_funnel = WorkspaceFunnel.query.filter_by(workspace=workspace).first()
    #print funnel_space.__dict__
    form.proposal_template.data = workspace_funnel.proposal_template
    form.status.data = workspace_funnel.status
    if form.validate_on_submit():
        form.populate_obj(workspace)
        workspace_funnel.status = workspace.status
        workspace_funnel.proposal_template = workspace.proposal_template
        print workspace.__dict__
        db.session.commit()
        flash(u"Edited Event '%s'" % workspace.title, 'success')
        return render_redirect(workspace.url_for(), code=303)
    return render_form(form=form, title="Edit Event", submit=u"Save",
        cancel_url=workspace.url_for(), ajax=True)
