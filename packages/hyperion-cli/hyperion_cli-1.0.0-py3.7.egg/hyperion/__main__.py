import asyncio
import logging

import click
import uvloop
from aiohttp import web
from colorama import Fore

from . import logger
from .api import app
from .cli import cli
from .models import util

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


@click.command()
@click.argument('postcodes', required=False, nargs=-1)
@click.option('--random', '-r', count=True)
@click.option('--bikes', '-b', is_flag=True)
@click.option('--crime', '-c', is_flag=True)
@click.option('--nearby', '-n', is_flag=True)
@click.option('--json', '-j', is_flag=True)
@click.option('--update-bikes', '-u', is_flag=True)
@click.option('--api-server', '-a', is_flag=True)
@click.option('--port', '-p', type=int, default=8000)
@click.option('--verbose', '-v', count=True)
def run(postcodes, random, bikes, crime, nearby, json, update_bikes, api_server, port, verbose):
    """
    Runs the program.

    :param postcodes: The postcode to search.
    :param random: The number of random postcodes to include.
    :param bikes: Includes a list of stolen bikes in that area.
    :param crime: Includes a list of committed crimes in that area.
    :param nearby: Includes a list of wikipedia articles in that area.
    :param json: Returns the data in json format.
    :param update_bikes:
    :param api_server: If given, the program will instead run a rest api.
    :param port: Defines the port to run the rest api on.
    :param verbose: The verbosity.
    """
    loop = asyncio.get_event_loop()

    log_levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    logging.basicConfig(level=log_levels[min(verbose, 2)])

    if update_bikes:
        logger.info("Force updating bikes.")
        loop.run_until_complete(util.update_bikes())

    if api_server:
        try:
            web.run_app(app, host='0.0.0.0', port=port)
        except asyncio.CancelledError:
            click.echo("Goodbye!")
    elif len(postcodes) > 0 or random > 0:
        exit(loop.run_until_complete(cli(postcodes, random, bikes=bikes, crime=crime, nearby=nearby, as_json=json)))
    else:
        click.echo(Fore.RED + "Either include a post code, or the --api-server flag.")


if __name__ == '__main__':
    run()
