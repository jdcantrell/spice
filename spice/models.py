from sqlalchemy import event, Column, Integer, String, DateTime, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from werkzeug.security import generate_password_hash

from shortid import ShortId

from spice.database import Base


class Timestamp(object):
  created = Column(DateTime, default=datetime.now())
  updated = Column(DateTime, default=datetime.now())

@event.listens_for(Timestamp, 'before_update', propagate=True)
def timestamp_before_update(mapper, connection, target):
  target.updated = datetime.now()


class User(Timestamp, Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True)
  username = Column(String(120), unique=True)
  password = Column(Text())

  def __init__(self, username, password):
    self.username = username
    self.password = generate_password_hash(password)

  def __repr__(self):
    return '<User %r>' % (self.username)

  def is_authenticated(self):
    return True

  def is_active(self):
    return True

  def is_anonymous(self):
    return False

  def get_id(self):
    return unicode(self.id)


class File(Timestamp, Base):
  __tablename__ = 'files'
  id = Column(Integer, primary_key=True)
  name = Column(String(255))
  path = Column(Text())
  filename = Column(Text())
  filetype = Column(String(255))
  handler = Column(String(255))
  key = Column(String(16))
  views = Column(Integer)
  access = Column(Enum('private', 'public', 'limited'))
  user_id = Column(Integer, ForeignKey('users.id'))
  user = relationship(User, primaryjoin=user_id == User.id)

  def __init__(self, name, filename, path, handler, filetype, access, user_id):
    self.name = name
    self.filename = filename
    self.path = path
    self.handler = handler
    self.filetype = filetype
    self.user_id = user_id
    self.access = access
    sid = ShortId()
    self.key = sid.generate()

    self.views = 0

  def __repr__(self):
    return '<File %r>' % (self.name)
