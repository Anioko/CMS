from app import db


class Workplace(db.Model):    
###Places of work to be listed here
    __tablename__ = 'workplaces'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))
    name = db.Column(db.String)
    description = db.Column(db.String)
    role = db.Column(db.String)
    role_description = db.Column(db.String)
    start_date = db.Column(db.DateTime, default=datetime.now, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    currently = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    country = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def __repr__(self):
        return u'<{self.__class__.__name__}: {self.id}>'.format(self=self)
