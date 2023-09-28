from distutils.command.config import config
import json
import configparser
import os

with open(os.path.join(os.path.dirname(__file__), 'config.json')) as config_file:
    config = json.load(config_file) 
    # export this to a config file

class Config:
    
    BASE_URL = config.get("BASE_URL")
    SECRET_KEY = config.get("SECRET_KEY")


    DATABASE_INFORMATION = ""
    JWT_SECRET_KEY = config.get("JWT_SECRET_KEY")

    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:%slocalhost/api" % config.get("DATABASE_USER_PASSWORD")

    # SQLALCHEMY_DATABASE_URI = "sqlite:////Users/krishnagaurav/flaskBackend/flaskapp/sqlite/test.db"
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    # CORS_HEADERS = "Content-Type"
    
    # Set  Twilio environment variables for your credentials
    # verify_sid = "VA279c1f534b4943a8e87c6a90dce22e37"
    twilio_account_sid = config.get("TWILIO_ACCOUNT_SID")
    twilio_default_from = config.get("TWILIO_DEFAULT_FROM")
    twilio_auth_token = config.get("TWILIO_AUTH_TOKEN")
    
    
    