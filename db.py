#include and add postgres sql to the project

import configparser

import psycopg2 # PostgreSql DataBase Adapter.

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if 'db' not  in g:
        #get credentials
        dbname = None
        user = None
        password = None
        db_conf = get_db_conf()
        if db_conf is not None:
            dbname = db_conf['DEFAULT']['DB_NAME']
            user = db_conf['DEFAULT']['DB_USER']
            password = db_conf['DEFAULT']['DB_PASSWORD']
        else:
            dbname = input('database name: ')
            user = input('user name: ')
            password = input('password name: ')

        g.db = psycopg2.connect("dbname = {} user = {} password = {}".format(dbname, user, password))
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)


def get_db_conf():
    config = configparser.ConfigParser()
    config.read('db.conf')
    if len(config) <= 0:
        return None

    return config
