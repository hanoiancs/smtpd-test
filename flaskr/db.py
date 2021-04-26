import os
import pymongo
from dotenv import load_dotenv
from flask import current_app, g


load_dotenv()


def init_app(app):
    app.teardown_appcontext(close_connection)


def get_connection():
    if "dbconnection" not in g:
        g.client = pymongo.MongoClient(
            host=os.getenv("DB_MONGO_HOST"),
            port=int(os.getenv("DB_MONGO_PORT")),
            username=os.getenv("DB_MONGO_USER"),
            password=os.getenv("DB_MONGO_PASSWORD"),
            authSource=os.getenv("DB_MONGO_AUTHENTICATION_DATABASE")
        )
    return g.client


def get_database():
    if 'db' not in g:
        g.db = get_connection()[os.getenv("DB_MONGO_DATABASE")]
    return g.db


def close_connection(e=None):
    client = g.pop('dbconnection', None)
    if client is not None:
        client.close()