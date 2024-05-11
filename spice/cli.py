import click


@click.group()
def cli():
    pass

@cli.command()
def process():
    from spice.models import File
    from spice.database import get_db
    from spice.handlers import get_handler_instance

    db_session = get_db()
    files = db_session.query(File).order_by(File.id.desc()).all()

    for record in files:
        handler = get_handler_instance(record)
        handler.process()
        db_session.add(handler.record)

        db_session.commit()
