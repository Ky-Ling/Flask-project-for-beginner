'''
Date: 2021-10-30 20:03:57
LastEditors: GC
LastEditTime: 2021-11-02 16:12:55
FilePath: \Flask-Project\website\__init__.py
'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, login_manager


# Define a new database
db = SQLAlchemy()
DB_NAME = "database.db"


# Creating a flask app
def create_app():
    app = Flask(__name__)

    # Encrypt or secure the cookies and session data related to our website
    app.config["SECRET_KEY"] = "hello world"

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    # Import the blueprint
    from .views import views
    from .auth import auth

    # Register the blueprint
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Note
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    # To tell the user how to load a user
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    # Check the database exists, if it does not exist, we will create this database.
    if not path.exists("website/" + DB_NAME):
        db.create_all(app=app)
        print("Created database!")
