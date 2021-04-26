from dotenv import load_dotenv
from flask import Flask


load_dotenv()


def create_app():
    # create and configure the app
    app = Flask(__name__)

    # Add database connection to application
    from . import db
    db.init_app(app)
    # Register Blueprints
    from . import mail
    app.register_blueprint(mail.bp)
    app.add_url_rule('/', endpoint='index', defaults={'id': ''})
    # Return application object
    return app


