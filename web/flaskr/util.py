import quopri
from email import message_from_string
from dateutil import tz

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