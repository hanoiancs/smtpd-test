import os
import argparse
import datetime
import pymongo
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
    parser.add_argument('-p', '--password', help='Input password', required=True)

    args = parser.parse_args()

    db = get_db()

    inserted_id = db.clients.insert_one({
        "username": args.user,
        "password": args.password,
        "created_at": datetime.datetime.utcnow()
    }).inserted_id

    print("Inserted new client: %s" % inserted_id)
