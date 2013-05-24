#!/usr/bin/env python
from hasweb import app, init_for
from hasweb.models import db
init_for('dev')
db.create_all()
app.run('0.0.0.0', debug=True, port=6400)
