from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/gig-opportunity-analyzer'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from app.routes import *
from app.models import *
from app.static import *

with app.app_context():
    db.create_all()