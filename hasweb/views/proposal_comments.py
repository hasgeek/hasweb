#! -*- coding: utf-8 -*-

from flask import flash, g, redirect, abort

from coaster.views import load_models, jsonp
from baseframe.forms import render_form

from hasweb import app
from hasweb.models import Profile, db, commentease
from hasweb.views.login import lastuser
from hasweb.models.workspace import Workspace
from hasweb.models.funnel import Proposal


@app.route('/<profile>/<workspace>/funnel/<proposal>/comments/<int:cid>/json', methods=['GET', 'POST'])
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Workspace, {'name': 'workspace', 'profile': 'profile'}, 'workspace'),
    (Proposal, {'url_name': 'proposal'}, 'proposal'), permission='view',
    kwargs=True
)
def jsoncomment(profile, workspace, proposal, kwargs):
    cid = kwargs['cid']
    comment = commentease.Comment.query.get(cid)
    if comment:
        return jsonp(message=comment.message)
    else:
        return jsonp(message='')


# FIXME:  Should be POST
@app.route('/<profile>/<workspace>/funnel/<proposal>/comments/<int:cid>/voteup', methods=['GET', 'POST'])
@lastuser.requires_login
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Workspace, {'name': 'workspace', 'profile': 'profile'}, 'workspace'),
    (Proposal, {'url_name': 'proposal'}, 'proposal'), permission='view',
    kwargs=True
)
def voteupcomment(profile, workspace, proposal, kwargs):
    cid = kwargs['cid']
    comment = commentease.Comment.query.get(cid)
    if not comment:
        abort(404)
    comment.votes.vote(g.user, votedown=False)
    db.session.commit()
    flash("Your vote has been recorded", "info")
    return redirect(proposal.url_for() + "#c%d" % cid)


# FIXME: Should be POST
@app.route('/<profile>/<workspace>/funnel/<proposal>/comments/<int:cid>/votedown', methods=['GET', 'POST'])
@lastuser.requires_login
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Workspace, {'name': 'workspace', 'profile': 'profile'}, 'workspace'),
    (Proposal, {'url_name': 'proposal'}, 'proposal'), permission='view',
    kwargs=True
)
def votedowncomment(profile, workspace, proposal, kwargs):
    cid = kwargs['cid']
    comment = commentease.Comment.query.get(cid)
    if not comment:
        abort(404)
    comment.votes.vote(g.user, votedown=True)
    db.session.commit()
    flash("Your vote has been recorded", "info")
    return redirect(proposal.url_for() + "#c%d" % cid)


# FIXME: Should be POST
@app.route('/<profile>/<workspace>/funnel/<proposal>/comments/<int:cid>/cancelvote', methods=['GET', 'POST'])
@lastuser.requires_login
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Workspace, {'name': 'workspace', 'profile': 'profile'}, 'workspace'),
    (Proposal, {'url_name': 'proposal'}, 'proposal'),
    permission='view', kwargs=True
)
def votecancelcomment(profile, workspace, proposal, kwargs):
    cid = kwargs['cid']
    comment = commentease.Comment.query.get(cid)
    if not comment:
        abort(404)
    comment.votes.cancelvote(g.user)
    db.session.commit()
    flash("Your vote has been withdrawn", "info")
    return redirect(proposal.url_for() + "#c%d" % cid)
