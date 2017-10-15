import datetime, re
from app import db, login_manager
from app import bcrypt
@login_manager.user_loader
def _user_loader(user_id):
    return User.query.get(int(user_id))

class User(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(255))
    username = db.Column(db.String(64), unique=True)
    active = db.Column(db.Boolean, default=True)
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

    # menerima password, return hashed version
    @staticmethod
    def make_password(plaintext):
        return bcrypt.generate_password_hash(plaintext)

    # mencocokan password input dan hash password
    def check_password(self, raw_password):
        return bcrypt.check_password_hash(self.password_hash, raw_password)

    # buat user dan sekaligus melakukan hashing pass before saving
    @classmethod
    def create(cls, username, password, **kwargs):
        return User(
            username=username,
            password_hash=User.make_password(password),
            **kwargs)

    # menerima user dan pass untuk dicek
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
    # status = db.Column(db.Integer, default=0, nullable=False)

    def __repr__(self):
        return '<Periode %s>' % self.periode

    def __unicode__(self):
        return self.periode.strftime("%B %Y") or ''


class Schedules(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    periode_id = db.Column(db.Integer, db.ForeignKey("periode.id"), nullable=False)
    bidan_id = db.Column(db.Integer, db.ForeignKey("bidan.id", ondelete='SET NULL'), nullable=True)
    name = db.Column(db.String(50), nullable=False)
    nip = db.Column(db.String(20), nullable=True)
    officer = db.Column(db.String(20), nullable=False)
    tim = db.Column(db.String(10), nullable=False)
    shift = db.Column(db.Text, default="", nullable=True)
    rest_shift = db.Column(db.Text, default="CLEAR", nullable=True)

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
    schedules = db.relationship("Schedules", backref="bidan")

    def __repr__(self):
        return '<Bidan %s>' % self.name

    def __unicode__(self):
        return self.name or ''