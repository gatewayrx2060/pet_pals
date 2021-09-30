def create_classes(db):
    class Pet(db.Model):
        __tablename__ = 'pets'

        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(64))
        lat = db.Column(db.Float)
        lon = db.Column(db.Float)

        def __repr__(self):
            return '<Pet %r>' % (self.name)
    return Pet

def create_classes2(db):
    class Large(db.Model):
        __tablename__ = 'large'

        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(64))
        lat = db.Column(db.Float)
        lon = db.Column(db.Float)

        def __repr__(self):
            return '<Large %r>' % (self.name)
    return Large
