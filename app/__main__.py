import logging
import json
import coloredlogs

from app.analitics import Analitics

coloredlogs.install(level=logging.INFO)


def app():
    logging.info('Starting app...')
    logging.info('App started.')
    try:
        f = open("input/result.json", "r", encoding="utf-8")
    except FileNotFoundError:
        logging.error('File not found! Put result.json in /input folder.')
        return

    logging.info('Reading result.json...')
    content = json.loads(f.read())
    f.close()
    logging.info('Reading result.json done.')

    logging.info('Running analitics...')
    analitics = Analitics(content)
    analitics.get_report()


if __name__ == '__main__':
    app()
