import json
import pandas as pd
from app import db
import app
from models import create_classes

# db.drop_all()
db.create_all()

# add new data for sqlite
for i in range(200000):
    record = app.Large(name=i, lat=i, lon=i)
    db.session.add(record)
db.session.commit()