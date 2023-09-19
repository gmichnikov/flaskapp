import os

basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE_URL = os.environ.get('DATABASE_URL').replace("postgres://", "postgresql://", 1)
SQLALCHEMY_DATABASE_URI = DATABASE_URL

SECRET_KEY = os.environ.get('SECRET_KEY')