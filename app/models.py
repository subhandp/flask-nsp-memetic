import datetime, re
from app import db

class User(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(255))
    username = db.Column(db.String(64), unique=True)
    active = db.Column(db.Boolean, default=True)
    admin = db.Column(db.Boolean, default=False)
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)

    def get_id(self):
        return unicode(self.id)

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def is_admin(self):
        return self.admin

    @staticmethod
    def make_password(plaintext):
        return bcrypt.generate_password_hash(plaintext)


    def check_password(self, raw_password):
        return bcrypt.check_password_hash(self.password_hash, raw_password)


    @classmethod
    def create(cls, username, password, **kwargs):
        return User(
            username=username,
            password_hash=User.make_password(password),
            **kwargs)


    @staticmethod
    def authenticate(username, password):
        user = User.query.filter(User.username == username).first()
        if user and user.check_password(password):
            return user
        return False

    def __unicode__(self):
        return self.name or ''


class Periode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    periode = db.Column(db.Date, default=datetime.datetime.now, nullable=False)
    schedules = db.relationship("Schedules", cascade="all,delete-orphan", backref="periode")

    def __repr__(self):
        return '<Periode %s>' % self.periode


class Schedules(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    periode_id = db.Column(db.Integer, db.ForeignKey("periode.id"), nullable=False)
    bidan_id = db.Column(db.Integer, db.ForeignKey("bidan.id"), nullable=False)
    #bidan = db.relationship("Bidan", cascade="all", backref="Schedules")
    name = db.Column(db.String(50), nullable=False)
    nip = db.Column(db.String(20), nullable=True)
    officer = db.Column(db.String(20), nullable=False)
    tim = db.Column(db.String(10), nullable=False)
    shift = db.Column(db.Text, nullable=True)
    rest_shift = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return '<Schedules %s>' % self.periode

    def __unicode__(self):
        return self.shift or ''


class Bidan(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    nip = db.Column(db.String(20))
    officer = db.Column(db.String(20), nullable=False)
    tim = db.Column(db.String(10), nullable=False)
    schedules = db.relationship("Schedules", cascade="all", backref="bidan")

    def __repr__(self):
        return '<Bidan %s>' % self.name

    def __unicode__(self):
        return self.name or ''