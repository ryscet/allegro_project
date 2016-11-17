# -*- coding: utf-8 -*-
"""
Website connects to sqlite db and display result. On button click analyze the db and produce some plots.
"""

from flask import Flask
app = Flask(__name__)

import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, redirect

import calc_trends as ct


app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'AllegroSales.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('SELECT offer_title, price, date_of_sale FROM Macs ORDER BY id DESC')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)


@app.route('/plots', methods = ['GET'])
def signup():
    ct.create_heatmap()
    return render_template('plots.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
