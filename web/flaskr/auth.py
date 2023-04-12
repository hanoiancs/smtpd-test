import functools
import click

from flask import (
    Blueprint
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_database

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/')
def auth():
    return '/auth/'


@bp.route('/login')
def login():
    pass


@bp.route('/logout')
def logout():
    pass


@bp.route('/register')
def register():
    pass


@bp.cli.command('create')
@click.argument('username')
def command_create_user(username):
    import random
    import string
    import datetime

    password = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

    inserted_id = get_database().clients.insert_one({
        "username": username,
        "password": password,
        "created_at": datetime.datetime.utcnow()
    }).inserted_id

    print("Inserted new client: %s\nUser: %s\nPassword: %s" % (inserted_id, username, password))

