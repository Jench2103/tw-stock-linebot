from typing import Any, Dict
import os
import json
import shutil

BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
CONFIG_EXAMPLE_FILE: str = os.path.join(BASE_DIR, 'config.example.json')
CONFIG_FILE: str = os.path.join(BASE_DIR, 'config.json')

if not os.path.isfile(CONFIG_FILE):
    shutil.copyfile(CONFIG_EXAMPLE_FILE, CONFIG_FILE)

with open(CONFIG_FILE, mode='r', encoding='utf-8') as file:
    CONFIG: Dict[str, Any] = json.load(file)
