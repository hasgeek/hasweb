# -*- coding: utf-8 -*-

from flask import render_template, abort, flash, request
from coaster.views import load_models, load_model
from baseframe.forms import render_form, render_redirect, render_delete_sqla
from hasweb import app
from hasweb.models import Profile, db
from hasweb.views.login import lastuser
from hasweb.models.workspace import Workspace, WorkspaceFunnel, WORKSPACE_FLAGS, funnel_status
from hasweb.models.funnel import Proposal
from hasweb.models.profile import PROFILE_TYPE
from hasweb.forms.workspace import FunnelSpaceForm


@app.route('/<profile>/<workspace>')
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Workspace, {'name': 'workspace', 'profile': 'profile'}, 'workspace'), permission='view'
    )
def workspace_view(profile, workspace):
    if workspace.has_funnel:
        workspace_funnel = WorkspaceFunnel.query.filter_by(workspace=workspace).first()
        if workspace:
            proposals = Proposal.query.filter_by(workspace_funnel=workspace_funnel).all()
        return render_template('workspace.html', profile=profile, workspace=workspace, proposals=proposals)
    return render_template('workspace.html', profile=profile, workspace=workspace)


@app.route('/<profile>/new', methods=['POST', 'GET'])
@lastuser.requires_login
@load_model(Profile, {'name': 'profile'}, 'profile', permission='new')
def workspace_new(profile):
    form = FunnelSpaceForm()
    if profile.type not in [PROFILE_TYPE.ORGANIZATION, PROFILE_TYPE.EVENTSERIES]:
        abort(403)
    if form.validate_on_submit():
        workspace = Workspace(profile=profile)
        #FIXME: Better way
        if WORKSPACE_FLAGS.FUNNEL in form.workspace_contains.data:
            workspace.enable_funnel()
            # FIXME: Use AJAX to show these options
            workspace.funnel.status = form.status.data
            workspace.funnel.proposal_template = form.proposal_template.data
        if WORKSPACE_FLAGS.FORUM in form.workspace_contains.data:
            workspace.enable_forum()
        if WORKSPACE_FLAGS.SCHEDULE in form.workspace_contains.data:
            workspace.disable_schedule()
        form.populate_obj(workspace)
        if not workspace.name:
            workspace.make_name()
        # workspace.status and workspace.proposal_template are temp variables that came from the form
        db.session.add(workspace)
        db.session.commit()
        flash(u"Created Event '%s'" % workspace.title, 'success')
        return render_redirect(workspace.url_for(), code=303)
    return render_form(form=form, title="New Workspace - Event", submit=u"Save",
        cancel_url=profile.url_for(), ajax=False)


@app.route('/<profile>/<workspace>/edit', methods=['POST', 'GET'])
@lastuser.requires_login
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Workspace, {'name': 'workspace', 'profile': 'profile'}, 'workspace'), permission='edit')
def workspace_edit(profile, workspace):
    #if profile.type != PROFILE_TYPE.ORGANIZATION:
    #    abort(403)
    form = FunnelSpaceForm(obj=workspace)
    if request.method == "GET":
        workspace_funnel = WorkspaceFunnel.query.filter_by(workspace=workspace).first()
        if workspace_funnel:
            form.proposal_template.data = workspace_funnel.proposal_template
        form.status.choices = [(type, funnel_status[type]) for type in funnel_status]
    if form.validate_on_submit():
        form.populate_obj(workspace)
        if WORKSPACE_FLAGS.FUNNEL in form.workspace_contains.data:
            workspace.enable_funnel()
            # FIXME: Use AJAX to show these options
            workspace.funnel.status = form.status.data
            workspace.funnel.proposal_template = form.proposal_template.data
        else:
            workspace.disable_funnel()
        if WORKSPACE_FLAGS.FORUM in form.workspace_contains.data:
            workspace.enable_forum()
        else:
            workspace.disable_forum()
        if WORKSPACE_FLAGS.SCHEDULE in form.workspace_contains.data:
            workspace.enable_schedule()
        else:
            workspace.disable_schedule()
        db.session.commit()
        flash(u"Edited Event '%s'" % workspace.title, 'success')
        return render_redirect(workspace.url_for(), code=303)
    return render_form(form=form, title="Edit Event", submit=u"Save",
        cancel_url=workspace.url_for(), ajax=True)


@app.route('/<profile>/<workspace>/delete', methods=['POST', 'GET'])
@lastuser.requires_login
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Workspace, {'name': 'workspace', 'profile': 'profile'}, 'workspace'), permission='delete')
def workspace_delete(profile, workspace):
    return render_delete_sqla(workspace, db, title=u"Confirm delete",
        message=u"Delete Workspace '%s'? This cannot be undone." % workspace.title,
        success=u"You have deleted workspace '%s'." % workspace.title,
        next=profile.url_for())
