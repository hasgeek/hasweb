# -*- coding: utf-8 -*-

from flask import render_template, abort, flash, g
from coaster.views import load_models, load_model
from baseframe.forms import render_form, render_redirect
from hasweb import app
from hasweb.models import Profile, db
from hasweb.views.login import lastuser
from hasweb.models.workspace import Workspace, WorkspaceFunnel
from hasweb.models.profile import PROFILE_TYPE
from hasweb.models.funnel import FunnelSpaceSection, Proposal
from hasweb.forms.workspace import ProposalForm, FunnelSectionForm


@app.route('/<profile>/<workspace>/funnel/new', methods=['GET', 'POST'], endpoint='funnel')
@lastuser.requires_login
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Workspace, {'name': 'workspace', 'profile': 'profile'}, 'workspace')
)
def funnel_new(profile, workspace):
    if not workspace.has_funnel:
        abort(403)
    form = ProposalForm()
    workspace_funnel = WorkspaceFunnel.query.filter_by(workspace=workspace).first()
    form.description.data = workspace_funnel.proposal_template
    form.section.choices = [(item.id, item.name) for item in FunnelSpaceSection.query.filter_by(workspace_funnel=workspace_funnel).all()]
    if form.validate_on_submit():
        proposal = Proposal(workspace_funnel=workspace_funnel)
        proposal.profile = Profile.query.filter_by(userid=g.user.userid).first()
        form.populate_obj(proposal)
        if not proposal.name:
            proposal.make_name()
        db.session.add(proposal)
        db.session.commit()
        flash(u"Created Proposal '%s'" % proposal.title, 'success')
        return render_redirect(proposal.url_for(), code=303)
    return render_form(form=form, title="New Proposal", submit=u"Save",
        cancel_url=workspace.url_for(), ajax=True)


@app.route('/<profile>/<workspace>/funnel/<proposal>', endpoint='proposal')
@lastuser.requires_login
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Workspace, {'name': 'workspace', 'profile': 'profile'}, 'workspace'),
    (Proposal, {'name': 'funnel'}, 'proposal'), permission='view'
)
def funnel_view(profile, workspace, proposal):
    return render_template('proposal.html', profile=profile, workspace=workspace, proposal=proposal)


@app.route('/<profile>/<workspace>/section/new', methods=['GET', 'POST'])
@lastuser.requires_login
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Workspace, {'name': 'workspace', 'profile': 'profile'}, 'workspace')
)
def section_new(profile, workspace):
    if not workspace.has_funnel:
        abort(403)
    form = FunnelSectionForm()
    if form.validate_on_submit():
        workspace_funnel = WorkspaceFunnel.query.filter_by(workspace=workspace).first()
        funnel_section = FunnelSpaceSection(workspace_funnel=workspace_funnel)
        form.populate_obj(funnel_section)
        if not funnel_section.name:
            funnel_section.make_name()
        db.session.add(funnel_section)
        db.session.commit()
        flash(u"Created Section '%s'" % funnel_section.title, 'success')
        return render_redirect(workspace.url_for(), code=303)
    return render_form(form=form, title="Create New Section", submit=u"Save",
        cancel_url=profile.url_for(), ajax=True)
