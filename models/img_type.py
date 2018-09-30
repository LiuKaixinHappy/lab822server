from app import db


class ImgType(db.Document):
    name = db.StringField(required=True)

