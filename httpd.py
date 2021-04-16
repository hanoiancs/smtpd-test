import os
import quopri
import pymongo
from dateutil import tz
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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/mails')
def get_mails():
    data = []
    mails = db.mails.find().limit(20).sort("_id", pymongo.DESCENDING)
    for mail in mails:
        # Decode content: Convert from quoted-printable to html
        content = quopri.decodestring(message_from_string(mail["content"]).get_payload()).decode()
        # Decode Subject
        subject = mail["subject"]
        # Convert created_at to local datetime
        created_at = mail["created_at"]
        created_at = created_at.replace(tzinfo=tz.tzutc())
        created_at = created_at.astimezone(tz.tzlocal()).strftime("%d-%m-%Y, %H:%M:%S")

        data.append({
            "id": str(mail["_id"]),
            "client_id": mail["client_id"],
            "from": mail["from"],
            "to": mail["to"],
            "subject": subject,
            "message": content,
            # "message": message_from_string(mail["content"]).get_payload(),
            "created_at": created_at
        })
    print(data)

    return jsonify(data)
