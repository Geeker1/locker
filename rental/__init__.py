from flask import Flask, render_template
import os
from .db import db
from rental.views import rental, auth

app = Flask(__name__)
app.register_blueprint(rental)
app.register_blueprint(auth)


def database_url(path):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + path
    env = os.getenv("FLASK_ENV")
    if env != "development":
        SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    return SQLALCHEMY_DATABASE_URI


@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404


app.config.from_object("rental.config.Config")
path = os.path.join(os.path.abspath(os.getcwd()), "test.db")
app.config["SQLALCHEMY_DATABASE_URI"] = database_url(path)
app.config.from_mapping(
    SECRET_KEY="skmfijkbkdsb732t6632467@*9834901912012soisudf")

db.init_app(app)


@app.cli.command("initdb")
def initdb_command():
    """ Initializes the database """
    db.drop_all()
    db.create_all()
    db.session.commit()
    print("Done all commits")

    print("Initialized the database")
