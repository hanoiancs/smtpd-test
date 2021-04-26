import pymongo
import math
from bson.objectid import ObjectId
from bson.errors import InvalidId
from flask import (
    Blueprint,
    Flask,
    g, 
    redirect,
    render_template,
    request,
    session,
    url_for,
    jsonify
)
from . import db
from .util import mail_to_json


bp = Blueprint('mail', __name__)


@bp.route('/', defaults={'id': ''})
@bp.route('/view/<id>')
def index(id):
    return render_template('index.html', id=id)


@bp.route('/api/mails')
def get_mails():
    # Paging
    try:
        page = int(request.args.get('page', 1))
    except ValueError as verr:
        page = 1
    page_size = 25
    offset = (page - 1) * page_size
    total_docs = db.get_database().mails.count_documents({})
    total_pages = math.ceil(total_docs / page_size)
    if page < 1:
        page = 1
    elif page > total_pages:
        page = total_pages
    
    # Query database to get list of mails
    mails = db.get_database().mails.find({}, {
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


@bp.route('/api/mails/<string:id>')
def get_mail(id):
    try:
        cursor = db.get_database().mails.find_one({"_id": ObjectId(id)});
        return {
            "success": True,
            "mail": mail_to_json(cursor)
        }
    except InvalidId as err:
        return {
            "success": False,
        }