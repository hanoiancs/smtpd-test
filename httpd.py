import os
import quopri
import eml_parser
import pymongo
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, url_for
from email import message_from_string

load_dotenv()

client = pymongo.MongoClient(
    host=os.getenv("DB_MONGO_HOST"),
    port=int(os.getenv("DB_MONGO_PORT")),
    username=os.getenv("DB_MONGO_USER"),
    password=os.getenv("DB_MONGO_PASSWORD"),
    authSource=os.getenv("DB_MONGO_AUTHENTICATION_DATABASE")
)
db = client[os.getenv("DB_MONGO_DATABASE")]
app = Flask(__name__)
ep = eml_parser.EmlParser()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/mails')
def get_mails():
    mails = []
    for mail in db.mails.find().sort("_id", pymongo.DESCENDING):
        content = quopri.decodestring(message_from_string(mail["content"]).get_payload()).decode()
        mails.append({
            "id": str(mail["_id"]),
            "client_id": mail["client_id"],
            "from": mail["from"],
            "to": mail["to"],
            "subject": mail["subject"],
            "message": content,
            # "message": message_from_string(mail["content"]).get_payload(),
            "created_at": mail["created_at"]
        })

    return jsonify(mails)
