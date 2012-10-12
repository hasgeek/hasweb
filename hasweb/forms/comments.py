#! -*- coding: utf-8 -*-

import flask.ext.wtf as wtf


class DeleteCommentForm(wtf.Form):
    comment_id = wtf.HiddenField('Comment', validators=[wtf.Required()])


class ConfirmDeleteForm(wtf.Form):
    """
    Confirm a delete operation
    """
    # The labels on these widgets are not used. See delete.html.
    delete = wtf.SubmitField(u"Delete")
    cancel = wtf.SubmitField(u"Cancel")
