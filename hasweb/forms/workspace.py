# -*- coding: utf-8 -*-

from flask import Markup
import flask.ext.wtf as wtf
from baseframe.forms import Form, RichTextField
from hasweb.models.workspace import funnel_status
from hasweb.models.funnel import proposal_status


__all__ = ['ProposalForm', 'FunnelSpaceForm', 'FunnelSectionForm']

DEFAULT_PROPOSAL_TEMPLATE = Markup("""
Objective

Description

Requirements

Slides

Links

""")


class FunnelSpaceForm(Form):
    title = wtf.TextField(u"Title", validators=[wtf.Required()],
        description=u"The name of the Workspace")
    description = RichTextField(u"Description")
    proposal_template = wtf.TextAreaField(u"Proposal Template", default=DEFAULT_PROPOSAL_TEMPLATE, validators=[wtf.Required()])
    status = wtf.SelectField(u"Status", coerce=int,
        choices=[(type, funnel_status[type]) for type in funnel_status], validators=[wtf.Required()])


class FunnelSectionForm(Form):
    title = wtf.TextField('Title', validators=[wtf.Required()])
    description = wtf.TextAreaField('Description', validators=[wtf.Required()])
    public = wtf.BooleanField('Public?')


class ProposalForm(Form):
    title = wtf.TextField('Title', validators=[wtf.Required()])
    description = wtf.TextAreaField(u"Description", default=u"",
        validators=[wtf.Required()])
    is_speaking = wtf.RadioField("Are you speaking?", coerce=int,
        choices=[(1, u"I will be speaking"),
                 (0, u"I’m proposing a topic for someone to speak on")])
    status = wtf.SelectField(u"Status", coerce=int,
        choices=[(type, proposal_status[type]) for type in proposal_status], validators=[wtf.Required()])
    bio = wtf.TextAreaField(u"Bio", default=u"", validators=[wtf.Required()])
    phone = wtf.TextField(u'Phone number', validators=[wtf.Required()],
        description=u"A phone number we can call you at to discuss your proposal, if required. "
            "Will not be displayed")
    section = wtf.SelectField(u'Section', coerce=int)
