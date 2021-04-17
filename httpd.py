import os
import quopri
import pymongo
import math
from dateutil import tz
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, url_for, request
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


def create_app():
    # create and configure the app
    app = Flask(__name__)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/mails')
    def get_mails():
        # Paging
        try:
            page = int(request.args.get('page', 1))
        except ValueError as verr:
            page = 1
        page_size = 25
        offset = (page - 1) * page_size
        total_docs = db.mails.count_documents({})
        total_pages = math.ceil(total_docs / page_size)
        if page < 1:
            page = 1
        elif page > total_pages:
            page = total_pages
        
        # Query database to get list of mails
        mails = db.mails.find().skip(offset).limit(page_size).sort("_id", pymongo.DESCENDING)

        # Prepare data to response
        data = []
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

        return jsonify({
            "paging": {
                "current": page,
                "total": total_pages,
                "page_size": page_size,
                "count_docs": total_docs,
                "from_doc": (offset + 1),
                "to_doc": (offset + len(data))
            },
            "docs": data
        })

    return app


