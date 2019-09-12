from json import load, dump
import logging
import sys


def get_logger(name: str) -> logging.Logger:
    '''returns a logger with the given name with an info level
    and write to stderr'''
    logger = logging.getLogger(name=name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler(stream=sys.stderr))
    return logger


logger = get_logger('dashedbot.utils')


def read_json(name: str, *, default={}):
    '''load json from a file'''
    try:
        with open(name, 'r') as f:
            logger.debug('loaded %s', name)
            return load(f)
    except FileNotFoundError:
        logger.debug('%s not found', name)
        return default


def write_json(obj, name: str):
    '''write json to a file'''
    with open(name, 'w') as f:
        dump(obj, f)
        logger.debug('wrote %s', name)


def map_values(f, d: dict) -> dict:
    return {k: f(v) for (k, v) in d.items()}
