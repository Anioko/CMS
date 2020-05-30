import json
import os

import cv2
from datetime import datetime
from logging import log
from time import time
from app import db

class Employment(db.Model):
    __tablename__ = 'employments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))
    minimum_pay = db.Column(db.Integer)
    maximum_pay = db.Column(db.Integer)
    minimum_duration = db.Column(db.String)
    currencies = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return u'<{self.__class__.__name__}: {self.id}>'.format(self=self)
