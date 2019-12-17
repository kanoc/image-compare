import os

from flask import Flask


_HERE = os.path.abspath(os.path.dirname(__file__))


DB_USER = os.environ['POSTGRES_USER']
DB_PWD = os.environ['POSTGRES_PASSWORD']
DB_NAME = os.environ['POSTGRES_DB']
DB_HOST = 'db'
DB_PORT = '5432'
APP_SECRET_KEY = os.environ['APP_SECRET_KEY']
UPLOAD_FOLDER = os.environ['UPLOAD_FOLDER']

app = Flask(
    __name__,
    static_url_path='/static',
    static_folder=os.path.join(_HERE, 'web/static'),
    template_folder=os.path.join(_HERE, 'web/templates')
)
app.secret_key = APP_SECRET_KEY
# Limit maximum allowed payload to 20 MB.
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
