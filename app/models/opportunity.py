import json
import os

import cv2
from datetime import datetime
from logging import log
from time import time
from app import db




class Opportunity(db.Model):
    __tablename__ = 'opportunities'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    title = db.Column(db.String)
    summary = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    country = db.Column(db.String)
    opportunity_type = db.Column(db.String)
    available_now = db.Column(db.String)
    location_type = db.Column(db.String)

    def __repr__(self):
        return u'<{self.__class__.__name__}: {self.id}>'.format(self=self)
