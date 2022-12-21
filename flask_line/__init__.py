from typing import Any, Dict
import os
import json
import shutil

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from linebot import LineBotApi, WebhookParser

BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
DATABASE_DIR: str = os.path.join(BASE_DIR, 'data')
DATABASE_PATH: str = os.path.join(DATABASE_DIR, 'data.sqlite')
CONFIG_EXAMPLE_FILE: str = os.path.join(BASE_DIR, 'config.example.json')
CONFIG_FILE: str = os.path.join(BASE_DIR, 'config.json')

for directory in [DATABASE_DIR]:
    if not os.path.isdir(directory):
        os.mkdir(directory)

if not os.path.isfile(CONFIG_FILE):
    shutil.copyfile(CONFIG_EXAMPLE_FILE, CONFIG_FILE)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DATABASE_PATH
db = SQLAlchemy(app)

app.app_context().push()

with open(CONFIG_FILE, mode='r', encoding='utf-8') as file:
    config: Dict[str, Any] = json.load(file)

line_bot_api = LineBotApi(config['line_developer']['channel_access_token'])
parser = WebhookParser(config['line_developer']['channel_secret'])

from . import entrypoint
