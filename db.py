#include and add postgres sql to the project

import psycopg2 # PostgreSql DataBase Adapter.

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if 'db' not  in g:
        g.db = psycopg2.connect("dbname = elections2019SV user = postgres password = secret")
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)