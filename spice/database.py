import click
from flask.cli import with_appcontext


from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(
    'sqlite:///%s' % app.config['DATABASE_FILE'],
    convert_unicode=True
)

db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

Base = declarative_base()
Base.query = db_session.query_property()

def close_db(exception=None):
    db_session.remove()


def init_db():
    import spice.models
    Base.metadata.create_all(bind=engine)


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.add_command(init_db_command)
