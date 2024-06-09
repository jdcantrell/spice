from sqlalchemy import event, Integer, String, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from datetime import datetime

from werkzeug.security import generate_password_hash

from shortid import ShortId

from spice.database import Base


class Timestamp(object):
    created: Mapped[datetime] = mapped_column(default=datetime.now())
    updated: Mapped[datetime] = mapped_column(default=datetime.now())


@event.listens_for(Timestamp, "before_update", propagate=True)
def timestamp_before_update(mapper, connection, target):
    target.updated = datetime.now()


class User(Timestamp, Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(120), unique=True)
    password: Mapped[str] = mapped_column(Text())

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)

    def __repr__(self):
        return "<User %r>" % (self.username)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


class File(Timestamp, Base):
    __tablename__ = "files"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    path: Mapped[str] = mapped_column(Text())
    filename: Mapped[str] = mapped_column(Text())
    filetype: Mapped[str] = mapped_column(String(255))
    handler: Mapped[str] = mapped_column(String(255))
    key: Mapped[str] = mapped_column(String(16))
    views: Mapped[int] = mapped_column(Integer)
    extra: Mapped[str] = mapped_column(Text())
    access: Mapped[str] = mapped_column(Enum("private", "public", "limited"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(primaryjoin=user_id == User.id)

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
        return "<File %r>" % (self.name)
