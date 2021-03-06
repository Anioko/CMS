from app import db


class PhotoGalleryItem(db.Model):
    __tablename__ = 'photogalleryitems'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    description = db.Column(db.String(512))
    file_id = db.Column(db.Integer, db.ForeignKey('files.id'))
    photogallery_id = db.Column(db.Integer, db.ForeignKey('photogalleries.id'))
    created_on = db.Column(db.DateTime)

    def __repr__(self):
        return '<PhotoGalleryItem {!r}'.format(self.title)
