#!/usr/bin/env python
import os
os.environ['ENVIRONMENT'] = "development"
from hasweb import app
from hasweb.models import db
db.create_all()
app.run('0.0.0.0', debug=True, port=6400)
