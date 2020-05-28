from flask import Flask
import os
from .db import db
from rental.views import rental, auth

app = Flask(__name__)
app.register_blueprint(rental)
app.register_blueprint(auth)

app.config.from_object("rental.config.Config")
path = os.path.join(os.path.abspath(os.getcwd()), "test.db")
if os.getenv("FLASK_ENV") == "DEVELOPMENT":
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + path
else:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
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
