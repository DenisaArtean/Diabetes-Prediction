
from flask.app import Flask
from flask_sqlalchemy import SQLAlchemy
import os



app = Flask(__name__, template_folder='templates', static_folder='static')

app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/diabetes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(12).hex()


db = SQLAlchemy(app)


