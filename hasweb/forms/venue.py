# -*- coding: utf-8 -*-

import flask.ext.wtf as wtf
from baseframe.forms import Form, RichTextField


__all__ = ['VenueCampusForm', 'VenueRoomForm']


class VenueCampusForm(Form):
    title = wtf.TextField("Name", description="Name of the venue", validators=[wtf.Required()])
    description = RichTextField("Notes", description="Notes about the venue",
        content_css="/static/css/editor.css")
    address1 = wtf.TextField("Address (line 1)", validators=[wtf.Required()])
    address2 = wtf.TextField("Address (line 2)", validators=[wtf.Optional()])
    postcode = wtf.TextField("Post code", validators=[wtf.Optional()])
    geonameid = wtf.IntegerField("Geonameid", validators=[wtf.Required()])
    latitude = wtf.DecimalField("Latitude", places=None, validators=[wtf.Optional(), wtf.NumberRange(-90, 90)])
    longitude = wtf.DecimalField("Longitude", places=None, validators=[wtf.Optional(), wtf.NumberRange(-180, 180)])


class VenueRoomForm(Form):
    title = wtf.TextField("Name", description="Name of the venue room", validators=[wtf.Required()])
    description = RichTextField("Notes", description="Notes about the venue room",
        content_css="/static/css/editor.css")
