import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    FLASK_APP = 'rental'
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = b'erir9347294382jdwbkj.//,/,'
    USERNAME = 'admin'
    PASSWORD = 'default'
