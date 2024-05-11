import click


@click.group()
def cli():
    pass


@cli.command()
@click.option("--name", prompt="Enter username")
@click.option(
    "--password", prompt="Enter password", hide_input=True, confirmation_prompt=True
)
def user_add(name, password):
    from spice.models import User
    from spice.database import db_session

    user = User(name, password)

    db_session.add(user)
    db_session.commit()

    print("User created: %r" % user.id)


@cli.command()
def create_db():
    from spice.database import init_db

    init_db()

    print("Database init")


@cli.command()
def process():
    from spice.models import File
    from spice.database import db_session
    from spice.handlers import get_handler_instance

    files = db_session.query(File).order_by(File.id.desc()).all()

    for record in files:
        handler = get_handler_instance(record)
        handler.process()
        db_session.add(handler.record)

        db_session.commit()
