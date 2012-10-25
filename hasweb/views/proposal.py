# -*- coding: utf-8 -*-

from datetime import datetime
from markdown import Markdown

from flask import render_template, abort, flash, g, request, redirect
from flask.ext.commentease import CommentForm, CsrfForm

from coaster.views import load_models
from baseframe.forms import render_form, render_redirect, render_delete_sqla

from hasweb import app
from hasweb.models import Profile, db, commentease
from hasweb.views.login import lastuser
from hasweb.models.workspace import Workspace, WorkspaceFunnel
from hasweb.models.funnel import Proposal
from hasweb.forms.workspace import ProposalForm, FunnelSectionForm, ConfirmSessionForm
from hasweb.forms.comments import DeleteCommentForm

markdown = Markdown(safe_mode="escape").convert


@app.route('/<profile>/<workspace>/funnel/new', methods=['GET', 'POST'])
@lastuser.requires_login
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Workspace, {'name': 'workspace', 'profile': 'profile'}, 'workspace'), permission='new'
    )
def funnel_new(profile, workspace):
    if not (workspace.has_funnel and workspace.funnel.is_open()):
        abort(403)
    form = ProposalForm()
    if request.method == "GET":
        form.description.data = workspace.funnel.proposal_template
    if form.validate_on_submit():
        proposal = Proposal(workspace_funnel=workspace.get_funnel())
        proposal.user = g.user
        form.populate_obj(proposal)
        proposal.description_html = markdown(proposal.description)
        if not proposal.name:
            proposal.make_name()
        proposal.make_id()
        proposal.votes.vote(g.user)
        db.session.add(proposal)
        db.session.commit()
        flash(u"Created Proposal '%s'" % proposal.title, 'success')
        return render_redirect(proposal.url_for(), code=303)
    return render_form(form=form, title="New Proposal", submit=u"Save",
        cancel_url=workspace.url_for(), ajax=True)


@app.route('/<profile>/<workspace>/funnel/<proposal>', methods=['POST', 'GET'])
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Workspace, {'name': 'workspace', 'profile': 'profile'}, 'workspace'),
    (Proposal, {'url_name': 'proposal'}, 'proposal'), permission='view'
)
def funnel_view(profile, workspace, proposal):
    comments = sorted(commentease.Comment.query.filter_by(commentspace=proposal.comments).order_by('created_at').all(),
        key=lambda c: c.votes.count, reverse=True)
    commentform = CommentForm()
    commentform.message.flags.markdown = True
    delcommentform = DeleteCommentForm()
    if request.method == 'POST':
        if request.form.get('form.id') == 'newcomment' and commentform.validate():
            if commentform.edit_id.data:
                comment = commentease.Comment.query.get(int(commentform.edit_id.data))
                if comment:
                    if comment.user == g.user:
                        comment.message = commentform.message.data
                        comment._message_html = markdown(comment.message)
                        comment.edited_at = datetime.utcnow()
                        flash("Your comment has been edited", "info")
                    else:
                        flash("You can only edit your own comments", "info")
                else:
                    flash("No such comment", "error")
            else:
                comment = commentease.Comment(user=g.user, commentspace=proposal.comments, message=commentform.message.data)
                if commentform.reply_to_id.data:
                    parent = commentease.Comment.query.get(int(commentform.reply_to_id.data))
                    if parent and parent.commentspace == proposal.comments:
                        comment.parent = parent
                comment._message_html = markdown(comment.message)
                proposal.comments.count += 1
                comment.votes.vote(g.user)  # Vote for your own comment
                db.session.add(comment)
                flash("Your comment has been posted", "info")
            db.session.commit()
            # Redirect despite this being the same page because HTTP 303 is required to not break
            # the browser Back button
            return render_redirect(proposal.url_for() + "#c" + str(comment.id), code=303)
        elif request.form.get('form.id') == 'delcomment' and delcommentform.validate():
            comment = commentease.Comment.query.get(int(delcommentform.comment_id.data))
            if comment:
                if comment.user == g.user:
                    comment.delete()
                    proposal.comments.count -= 1
                    db.session.commit()
                    flash("Your comment was deleted.", "info")
                else:
                    flash("You did not post that comment.", "error")
            else:
                flash("No such comment.", "error")
            return render_redirect(proposal.url_for(), code=303)
    confirmform = ConfirmSessionForm()
    return render_template('proposal.html', workspace=workspace, proposal=proposal,
        comments=comments, commentform=commentform, delcommentform=delcommentform, csrfform=CsrfForm(),
        breadcrumbs=[(proposal.url_for(), workspace.title)], confirmform=confirmform)


@app.route('/<profile>/<workspace>/funnel/<proposal>/edit', methods=['POST', 'GET'])
@lastuser.requires_login
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Workspace, {'name': 'workspace', 'profile': 'profile'}, 'workspace'),
    (Proposal, {'url_name': 'proposal'}, 'proposal'), permission='view'
)
def funnel_edit(profile, workspace, proposal):
    if proposal.user.userid != g.user.userid:
        abort(403)
    form = ProposalForm(obj=proposal)
    workspace_funnel = WorkspaceFunnel.query.filter_by(workspace=workspace).first()
    if request.method == 'GET':
        form.description.data = workspace_funnel.proposal_template
    if form.validate_on_submit():
        form.populate_obj(proposal)
        if not proposal.name:
            proposal.make_name()
        db.session.commit()
        flash(u"Edited Proposal '%s'" % proposal.title, 'info')
        return render_redirect(proposal.url_for(), code=303)
    return render_form(form=form, title="Edit Proposal", submit=u"Save",
        cancel_url=workspace.url_for(), ajax=True)


@app.route('/<profile>/<workspace>/funnel/<proposal>/delete', methods=['POST', 'GET'])
@lastuser.requires_login
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Workspace, {'name': 'workspace', 'profile': 'profile'}, 'workspace'),
    (Proposal, {'url_name': 'proposal'}, 'proposal'), permission='delete'
)
def funnel_delete(profile, workspace, proposal):
    return render_delete_sqla(proposal, db, title=u"Confirm delete",
        message=u"Delete Proposal '%s'? This cannot be undone." % proposal.title,
        success=u"You have deleted proposal '%s'." % proposal.title,
        next=workspace.url_for())


@app.route('/<profile>/<workspace>/funnel/<proposal>/confirm', methods=['POST'])
@lastuser.requires_permission('siteadmin')
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Workspace, {'name': 'workspace', 'profile': 'profile'}, 'workspace'),
    (Proposal, {'url_name': 'proposal'}, 'proposal'), permission='delete'
)
def confirm_session(profile, workspace, proposal):
    form = ConfirmSessionForm()
    if form.validate_on_submit():
        proposal.confirmed = not proposal.confirmed
        db.session.commit()
        if proposal.confirmed:
            flash("This proposal has been confirmed.", 'success')
        else:
            flash("This session has been cancelled.", 'success')
    return redirect(proposal.url_for())


@app.route('/<profile>/<workspace>/funnel/<proposal>/action', methods=['GET', 'POST'])
@lastuser.requires_login
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Workspace, {'name': 'workspace', 'profile': 'profile'}, 'workspace'),
    (Proposal, {'url_name': 'proposal'}, 'proposal')
)
def funnel_action(profile, workspace, proposal):
    print commentease.vote_action(proposal.votes)
    return "Done"


@app.route('/<profile>/<workspace>/funnel/<proposal>/cancelvote', endpoint='cancelsessionvote')
@lastuser.requires_login
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Workspace, {'name': 'workspace', 'profile': 'profile'}, 'workspace'),
    (Proposal, {'url_name': 'proposal'}, 'proposal'), permission='view'
)
def votecancelsession(profile, workspace, proposal):
    #FIXME: GET -> POST
    proposal.votes.cancelvote(g.user)
    db.session.commit()
    flash("Your vote has been withdrawn", "info")
    return redirect(proposal.url_for())


# URLS for proposal voting
# FIXME: This voting method uses GET but makes db changes. Not correct. Should be POST
@app.route('/<profile>/<workspace>/funnel/<proposal>/voteup', endpoint='voteupsession')
@lastuser.requires_login
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Workspace, {'name': 'workspace', 'profile': 'profile'}, 'workspace'),
    (Proposal, {'url_name': 'proposal'}, 'proposal'), permission='view'
)
def voteupsession(profile, workspace, proposal):
    proposal.votes.vote(g.user, votedown=False)
    db.session.commit()
    flash("Your vote has been recorded", "info")
    return redirect(proposal.url_for())


# FIXME: This voting method uses GET but makes db changes. Not correct. Should be POST
@app.route('/<profile>/<workspace>/funnel/<proposal>/votedown', endpoint='votedownsession')
@lastuser.requires_login
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Workspace, {'name': 'workspace', 'profile': 'profile'}, 'workspace'),
    (Proposal, {'url_name': 'proposal'}, 'proposal'), permission='view'
)
def votedownsession(profile, workspace, proposal):
    proposal.votes.vote(g.user, votedown=False)
    db.session.commit()
    flash("Your vote has been recorded", "info")
    return redirect(proposal.url_for())


# Route for sections in proposal
"""
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
        funnel_section = WorkspaceFunnelSection(workspace_funnel=workspace_funnel)
        form.populate_obj(funnel_section)
        if not funnel_section.name:
            funnel_section.make_name()
        db.session.add(funnel_section)
        db.session.commit()
        flash(u"Created Section '%s'" % funnel_section.title, 'success')
        return render_redirect(workspace.url_for(), code=303)
    return render_form(form=form, title="Create New Section", submit=u"Save",
        cancel_url=profile.url_for(), ajax=True)
"""
