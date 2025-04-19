import os

class Config:
    # Secret key
    SECRET_KEY = 'super-secret-key'  # you can change this to something more secure

    # Database config
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'aesthetichacks.in.com@gmail.com'
    MAIL_PASSWORD = 'auxypydwamvkmfcb'
