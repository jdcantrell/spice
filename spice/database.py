from flask import current_app, g
import click

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, DeclarativeBase


class Base(DeclarativeBase):
    pass


def get_db():
    if "db" not in g:
        engine = create_engine(
            f"sqlite:///{current_app.config['DATABASE_FILE']}", echo=True, future=True
        )

        g.db = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=engine)
        )

    return g.db


def close_db(exception=None):
    get_db().remove()


def init_db():
    engine = create_engine(
        f"sqlite:///{current_app.config['DATABASE_FILE']}", echo=True, future=True
    )

    Base.metadata.create_all(bind=engine)


@click.command("init-db")
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


@click.command("create-user")
@click.option("--name", prompt="Enter username")
@click.password_option()
def create_user(name, password):
    from spice.models import User

    db = get_db()

    user = User(name, password)

    db.add(user)
    db.commit()
    click.echo("Added {} to the user database.".format(user.username))


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(create_user)
