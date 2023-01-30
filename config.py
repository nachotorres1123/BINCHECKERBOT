import os
import json
from queue import Queue
from os import path, getenv


class Config:
    API_ID = getenv("ID", "ID DE DESARROLLADOR DE TELEGRAM")
    API_HASH = getenv("HASH", "HASH DE LA API DE TELEGRAM")
    BOT_TOKEN = getenv("TOKEN", "TOKEN DE BOT")
