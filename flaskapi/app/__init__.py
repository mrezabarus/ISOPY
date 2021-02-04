from flask import Flask
from flask_cors import CORS, cross_origin
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager


app = Flask(__name__)
CORS(app, support_credentials=True)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app,db)

jwt = JWTManager(app)


from app.model import user, dosen, mahasiswa
from app import routes