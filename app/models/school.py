import json
import os

import cv2
from datetime import datetime, date
from logging import log
from time import time
from app import db

class School(db.Model): 
###Schools to be listed here
    __tablename__ = 'schools'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))
    name = db.Column(db.String)
    description = db.Column(db.String)
    grading = db.Column(db.String)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    currently = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    country = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())


