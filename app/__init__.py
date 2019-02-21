from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from apscheduler.schedulers.background import BackgroundScheduler

socketio = SocketIO()

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
socketio.init_app(app)


from app import routes, models

 # init BackgroundScheduler job
scheduler = BackgroundScheduler()
scheduler.add_job(models.Pool.delete_expire_Pool, trigger='interval', seconds=99999)
scheduler.start()

models.reset_attack_num()


