# coding=utf8
import click
from app import create_app

@click.group()
def cli():
    pass

@click.command()
@click.option('--bind', default='127.0.0.1', help='host name for listen')
@click.option('--port', default=8000, help='port for listen')
def runserver(bind, port):
    app = create_app()
    app.run(host=bind, port=port, debug=True)

cli.add_command(runserver)
cli()