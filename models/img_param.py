from app import db


class ImgParam(db.Document):

    type = db.StringField(required=True)
    name = db.StringField(required=True)
    value = db.ListField()
    limit = db.StringField()
    pName = db.StringField()

