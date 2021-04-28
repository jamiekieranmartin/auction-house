import os
from flask import Flask
from flask.templating import render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.exceptions import HTTPException

db = SQLAlchemy()
SQLALCHEMY_TRACK_MODIFICATIONS = True


def create_app():
    '''Initialises the web application'''
    # this is the name of the module/package that is calling this app
    app = Flask(__name__)
    app.secret_key = 'secretsmellypoo'
    # set the app configuration data
    db_uri = 'sqlite:///marketplace.sqlite'

    if 'DATABASE_URL' in os.environ:
        db_uri = os.environ['DATABASE_URL']

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    # initialize db with flask app
    db.init_app(app)

    bootstrap = Bootstrap(app)

    # initialize the login manager
    login_manager = LoginManager()

    # set the name of the login function that lets user login
    # in our case it is auth.login (blueprintname.viewfunction name)
    from .auth.models import Anonymous
    login_manager.anonymous_user = Anonymous
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = "danger"
    login_manager.init_app(app)

    # TODO: I put the user_loader in the startup here
    from .auth.models import User
    from .item.models import Item
    # create a user loader function takes userid and returns User

    @login_manager.user_loader
    def load_user(user_id):
        # however you get your users - bridge the gap
        return User.query.get(int(user_id))

    # custom error handling
    @app.errorhandler(HTTPException)
    def handle_error(error):
        return render_template("error.html", error=error)

    # @importing views module here to avoid circular references
    # a commonly used practice.

    from .views import bp
    app.register_blueprint(bp)

    from auction.auth.views import auth_bp
    app.register_blueprint(auth_bp)

    from auction.item.views import item_bp
    app.register_blueprint(item_bp)

    from auction.bid.views import bid_bp
    app.register_blueprint(bid_bp)

    from auction.watchlist.views import watchlist_bp
    app.register_blueprint(watchlist_bp)

    with app.app_context():
        db.create_all()

    return app
