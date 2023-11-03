from flask import Flask
from config import create_tables
# from flask_sqlalchemy import SQLAlchemy
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s | %(levelname)s: %(message)s')

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'


if __name__ == '__main__':
    create_tables()
    app.run(host='0.0.0.0',port=8080)