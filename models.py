from app_config import db
import datetime
from flask_login import UserMixin

class Users(db.Model, UserMixin):
  user_id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(120),nullable=False,unique=False)
  last_name = db.Column(db.String(120),nullable=False,unique=False)
  email = db.Column(db.String(255),nullable=False,unique=True)
  password = db.Column(db.String(120),nullable=False)
  created_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

  def get_id(self):
      return (self.user_id)