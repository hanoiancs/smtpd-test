from email.policy import default
import os
import quopri
from bson.errors import InvalidId
import pymongo
import math
from dateutil import tz
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, url_for, request
from email import message_from_string
from bson.objectid import ObjectId

load_dotenv()

client = pymongo.MongoClient(
    host=os.getenv("DB_MONGO_HOST"),
    port=int(os.getenv("DB_MONGO_PORT")),
    username=os.getenv("DB_MONGO_USER"),
    password=os.getenv("DB_MONGO_PASSWORD"),
    authSource=os.getenv("DB_MONGO_AUTHENTICATION_DATABASE")
)
db = client[os.getenv("DB_MONGO_DATABASE")]


def mail_to_json(mail):
    """
    Convert MongoDB mail document to JSON object.
    """
    # Decode content: Convert from quoted-printable to html
    if "content" in mail:
        content = quopri\
                .decodestring(message_from_string(mail["content"]).get_payload())\
                .decode()
    else:
        content = ""
    # Decode Subject
    subject = mail["subject"]
    # Convert created_at to local datetime
    created_at = mail["created_at"]
    created_at = created_at\
        .replace(tzinfo=tz.tzutc()).astimezone(tz.tzlocal())\
        .strftime("%d-%m-%Y, %H:%M:%S")

    return {
        "id": str(mail["_id"]),
        "client_id": mail["client_id"],
        "from": mail["from"],
        "to": mail["to"],
        "subject": subject,
        "message": content,
        "created_at": created_at
    }


def create_app():
    # create and configure the app
    app = Flask(__name__)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/', defaults={'id': ''})
    @app.route('/view/<id>')
    def index(id):
        return render_template('index.html', id=id)

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
        mails = db.mails.find({}, {
            "_id": 1,
            "client_id": 1, 
            "from": 1,
            "to": 1,
            "subject": 1,
            "created_at": 1
        }).skip(offset).limit(page_size).sort("_id", pymongo.DESCENDING)

        # Prepare data to response
        data = []
        for mail in mails:
            data.append(mail_to_json(mail))

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
    
    @app.route('/mail/<string:id>')
    def get_mail(id):
        try:
            cursor = db.mails.find_one({"_id": ObjectId(id)});
            return {
                "success": True,
                "mail": mail_to_json(cursor)
            }
        except InvalidId as err:
            return {
                "success": False,
            }

    # Return Application Object
    return app


