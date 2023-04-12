import datetime
import os
import logging
import email.header
import asyncio
import pymongo

from dotenv import load_dotenv
from email import message_from_bytes
from aiosmtpd.controller import Controller
from aiosmtpd.smtp import (
    SMTP,
    Session,
    Envelope,
    AuthResult,
    LoginPassword
)


load_dotenv()

client = pymongo.MongoClient(
    host=os.getenv("DB_MONGO_HOST"),
    port=int(os.getenv("DB_MONGO_PORT")),
    username=os.getenv("DB_MONGO_USER"),
    password=os.getenv("DB_MONGO_PASSWORD"),
    authSource=os.getenv("DB_MONGO_AUTHENTICATION_DATABASE")
)

db = client[os.getenv("DB_MONGO_DATABASE")]

print(f"DB_MONGO_HOST: {os.getenv('DB_MONGO_HOST')}")

def decode_mime_words(s):
    return u''.join(
        word.decode(encoding or 'utf8') if isinstance(word, bytes) else word
        for word, encoding in email.header.decode_header(s))


class MongoDbHandler:
    async def handle_DATA(self, server: SMTP, session: Session, envelope: Envelope):
        message = message_from_bytes(envelope.content)
        db.mails.insert_one({
            "client_id": session.auth_data['id'],
            "from": envelope.mail_from,
            "to": envelope.rcpt_tos,
            "subject": decode_mime_words(message.get("Subject")),
            "content": envelope.content.decode('utf', errors='replace'),
            "created_at": datetime.datetime.utcnow(),
        })
        return '250 OK'


class Authenticator:
    def __init__(self):
        pass

    def __call__(self, server: SMTP, session: Session, envelope: Envelope, mechanism: str, auth_data):
        fail_nothandled = AuthResult(success=False, handled=False)
        if mechanism not in ("LOGIN", "PLAIN"):
            return fail_nothandled
        if not isinstance(auth_data, LoginPassword):
            return fail_nothandled
        
        username = auth_data.login.decode()
        password = auth_data.password.decode()

        auth_client = db.clients.find_one({
            "username": username,
            "password": password
        })

        if auth_client:
            return AuthResult(success=True, auth_data={"id": str(auth_client['_id'])})
        
        return fail_nothandled


async def amain(loop):
    handler = MongoDbHandler()

    cont = Controller(
        handler,
        hostname=os.getenv('SMTP_SERVER_HOSTNAME'),
        port=int(os.getenv('SMTP_SERVER_PORT')),
        authenticator=Authenticator(),
        auth_required=os.getenv('SMTP_SERVER_AUTH_REQUIRED').lower() == 'true',
        auth_require_tls=os.getenv('SMTP_SERVER_AUTH_REQUIRE_TLS').lower() == 'true'
    )

    cont.start()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    loop.create_task(amain(loop))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
