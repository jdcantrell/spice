import click
from flask.cli import with_appcontext
from flask import current_app, g


from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def get_db():
    if "db" not in g:
        engine = create_engine(
            "sqlite:///%s" % current_app.config["DATABASE_FILE"], convert_unicode=True
        )

        g.db = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=engine)
        )

        Base.query = g.db.query_property()

    return g.db


def close_db(exception=None):
    get_db().remove()


def init_db():
    engine = create_engine(
        "sqlite:///%s" % current_app.config["DATABASE_FILE"], convert_unicode=True
    )

    import spice.models

    Base.metadata.create_all(bind=engine)


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
