# -*- coding: utf-8 -*-

from hasweb.models import db, BaseScopedNameMixin


# TODO: Check with Flask-tease and sort out for votes, comments
class ProposalSpace(BaseScopedNameMixin, db.Model):
    __tablename__ = 'proposal_space'


class ProposalSpaceSection(BaseScopedNameMixin, db.Model):
    __tablename__ = 'proposal_space_section'


class Proposal(BaseScopedNameMixin, db.Model):
    __tablename__ = 'proposal'
