# -*- coding: utf-8 -*-

from hasweb.models import db, BaseScopedNameMixin

__all__ = ['Workspace']


# TODO: Either make this a polymorphic base class with different kinds of workspaces possible
# or establish 1:1 relationships to tables that contain data for each type of workspace
class Workspace(BaseScopedNameMixin, db.Model):
    __tablename__ = 'workspace'
