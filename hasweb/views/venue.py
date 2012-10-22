# -*- coding: utf-8 -*-

from flask import render_template, abort, flash, g

from coaster.views import load_model, load_models

from baseframe.forms import render_form, render_redirect, render_delete_sqla

from hasweb import app, lastuser
from hasweb.models import db
from hasweb.forms.venue import VenueCampusForm, VenueRoomForm
from hasweb.models.venue import VenueCampus, VenueRoom
from hasweb.models.profile import Profile


@app.route('/venue/new', methods=['GET', 'POST'])
@lastuser.requires_login
def venue_new():
    form = VenueCampusForm()
    #profile = Profile.query.filter_by(userid=g.user.userid).first()
    if form.validate_on_submit():
        venue = VenueCampus(user=g.user)
        form.populate_obj(venue)
        if not venue.name:
            venue.make_name()
        db.session.add(venue)
        db.session.commit()
        flash(u"Created new venue '%s'" % venue.title, 'success')
        return render_redirect(venue.url_for(), code=303)
    return render_form(form=form, title="Create New venue", submit=u"Save",
        cancel_url=g.user.profile_url, ajax=True)


@app.route('/venue/<venue>', methods=['GET'])
@load_model(VenueCampus, {'name': 'venue'}, 'venue_campus', permission='view')
def venue_view(venue_campus):
    return render_template('venue.html', venue=venue_campus)


@app.route('/venue/<venue>/edit', methods=['POST', 'GET'])
@lastuser.requires_login
@load_model(VenueCampus, {'name': 'venue'}, 'venue_campus', permission='edit')
def venue_edit(venue_campus):
    form = VenueCampusForm(obj=venue_campus)
    if form.validate_on_submit():
        form.populate_obj(venue_campus)
        if not venue_campus.name:
            venue_campus.make_name()
        db.session.commit()
        flash(u"Edited Venue details '%s'" % venue_campus.title, 'info')
        return render_redirect(venue_campus.url_for(), code=303)
    return render_form(form=form, title="Edit Venue Proposal", submit=u"Save",
        cancel_url=venue_campus.user.profile_url, ajax=True)


@app.route('/venue/<venue>/delete', methods=['POST', 'GET'])
@lastuser.requires_login
@load_model(VenueCampus, {'name': 'venue'}, 'venue_campus', permission='delete')
def venue_delete(venue_campus):
    return render_delete_sqla(venue_campus, db, title=u"Confirm delete",
        message=u"Delete Venue '%s'? This cannot be undone." % venue_campus.title,
        success=u"You have deleted workspace '%s'." % venue_campus.title,
        next=venue_campus.user.profile_url)


@app.route('/venue/<venue>/new', methods=['GET', 'POST'])
@lastuser.requires_login
@load_model(VenueCampus, {'name': 'venue'}, 'venue_campus', permission='new')
def venue_campus_new(venue_campus):
    form = VenueRoomForm()
    if form.validate_on_submit():
        venue_room = VenueRoom(campus=venue_campus)
        form.populate_obj(venue_room)
        if not venue_room.name:
            venue_room.make_name()
        db.session.add(venue_room)
        db.session.commit()
        flash(u"Created new venue campus detail '%s'" % venue_room.title, 'success')
        return render_redirect(venue_campus.url_for(), code=303)
    return render_form(form=form, title="Venue Room Detail", submit=u"Save",
        cancel_url=venue_campus.url_for(), ajax=True)


@app.route('/venue/<venue>/<room>/delete', methods=['POST', 'GET'])
@lastuser.requires_login
@load_models(
    (VenueCampus, {'name': 'venue'}, 'venue_campus'),
    (VenueRoom, {'name': 'room', 'campus': 'venue_campus'}, 'venue_room'))
def venue_campus_delete(venue_campus, venue_room):
    return render_delete_sqla(venue_room, db, title=u"Confirm delete",
        message=u"Delete Venue Room'%s'? This cannot be undone." % venue_room.title,
        success=u"You have deleted workspace '%s'." % venue_room.title,
        next=venue_campus.url_for())


@app.route('/venue/<venue>/<room>/edit', methods=['POST', 'GET'])
@lastuser.requires_login
@load_models(
    (VenueCampus, {'name': 'venue'}, 'venue_campus'),
    (VenueRoom, {'name': 'room', 'campus': 'venue_campus'}, 'venue_room'), permission='edit')
def venue_campus_edit(venue_campus, venue_room):
    form = VenueRoomForm(obj=venue_room)
    if form.validate_on_submit():
        form.populate_obj(venue_room)
        if not venue_room.name:
            venue_room.make_name()
        db.session.commit()
        flash(u"Edited Venue Campus details '%s'" % venue_room.title, 'info')
        return render_redirect(venue_campus.url_for(), code=303)
    return render_form(form=form, title="Venue Room", submit=u"Save",
        cancel_url=venue_campus.url_for(), ajax=True)

"""
@app.route('/venues', methods=['GET'])
def venues_edit():
    venues = Venue.query.all()
    return render_template('venues.html', venues=venues)
"""
