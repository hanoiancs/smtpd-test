import os
import argparse
import datetime
import pymongo
import random
import string
from dotenv import load_dotenv

load_dotenv()


def get_db_client() -> pymongo.MongoClient:
    return pymongo.MongoClient(
        host=os.getenv("DB_MONGO_HOST"),
        port=int(os.getenv("DB_MONGO_PORT")),
        username=os.getenv("DB_MONGO_USER"),
        password=os.getenv("DB_MONGO_PASSWORD"),
        authSource=os.getenv("DB_MONGO_AUTHENTICATION_DATABASE")
    )


def get_db():
    client = get_db_client()
    return client[os.getenv("DB_MONGO_DATABASE")]


__author__ = 'quanta@ecomobi.com'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create SMTP auth username and password.')
    parser.add_argument('-u', '--user', help='Input username', required=True)
    parser.add_argument('-p', '--password', help='Input password', required=False)

    args = parser.parse_args()

    db = get_db()

    username = args.user
    password = args.password
    # Generate random password
    if not password:
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

    inserted_id = db.clients.insert_one({
        "username": username,
        "password": password,
        "created_at": datetime.datetime.utcnow()
    }).inserted_id

    print("Inserted new client: %s\nUser: %s\nPassword: %s" % (inserted_id, username, password))
