from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO


socketio = SocketIO()

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
socketio.init_app(app)


from app import routes, models

models.reset_attack_num()