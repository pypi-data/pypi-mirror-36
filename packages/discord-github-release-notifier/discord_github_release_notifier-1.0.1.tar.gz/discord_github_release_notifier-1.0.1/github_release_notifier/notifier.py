#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, json, os, requests, logging, re, threading
from .webhook import get, get_list
from .parser import parse
from pathlib import Path

__DEFAULT_FILE__ = '/root/.github_release_notifier/versions'


def version_compare(check, current):
    def normalize(v):
        return int(re.sub(r'[^0-9]', "", v))

    return normalize(check) > normalize(current)

def _call_webhook(webhook, entry, logger):
    logger.info("Hook call : %s / %s" % (webhook, json.dumps(entry)))
    try:
        requests.post(webhook, json=entry)
    except:
        logger.error("Error occured : %s" % (sys.exc_info()[0]))

def run(file=__DEFAULT_FILE__):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    updated = {}
    for package in get_list():
        logger.info("Checking %s..." % package)
        for entry in parse(package):
            logger.debug("\tComparing %s with %s" % (entry['version'], get_version(package)))
            if version_compare(entry['version'], get_version(package)):
                database = _get_database(file)
                database[package] = entry['version']
                _set_database(database, file)
                updated[package] = entry['version']
                for webhook in get(package):
                    threading.Thread(target=_call_webhook, args=(webhook, entry, logger,)).start()
#            return updated# TODO: Add option to only check last
    return updated


def _get_database(file=__DEFAULT_FILE__):
    database = {}
    if Path(file).is_file():
        database = json.loads(open(file, "r").read())
    return database


def _set_database(database, filepath=__DEFAULT_FILE__):
    dirname = os.path.dirname(filepath)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    file = open(filepath, "w+")
    file.write(json.dumps(database))
    file.close()


def get_version(package, file=__DEFAULT_FILE__):
    database = _get_database(file)
    try:
        return database[package]
    except KeyError:
        return '0.0.0'


def main():
    print(run())


if __name__ == "__main__":
    main()
