import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from linebot import LineBotApi, WebhookParser

from config import CONFIG, DATABASE_PATH

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DATABASE_PATH
db = SQLAlchemy(app)

app.app_context().push()

line_bot_api = LineBotApi(CONFIG['line_developer']['channel_access_token'])
parser = WebhookParser(CONFIG['line_developer']['channel_secret'])

from . import entrypoint
