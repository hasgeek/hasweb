# -*- coding: utf-8 -*-

from . import db, BaseScopedNameMixin

__all__ = ['Workspace']


class WorkspaceType:
    UNDEFINED = 0
    EVENT = 1
    FORUM = 2

workspace_types = {
    0: u"undefined",
    1: u"event",
    2: u"forum"
    }


# TODO: Either make this a polymorphic base class with different kinds of workspaces possible
# or establish 1:1 relationships to tables that contain data for each type of workspace
class Workspace(BaseScopedNameMixin, db.Model):
    __tablename__ = 'workspace'

    workspace_type = db.Column(db.Integer, default=WorkspaceType.UNDEFINED, nullable=False)
