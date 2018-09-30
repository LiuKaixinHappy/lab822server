from app import db


class ImgOperation(db.Document):
    name = db.StringField(required=True)
    code = db.StringField(required=True)
    type = db.ListField(db.EmbeddedDocumentField('ImgType'))
    params = db.ListField(db.EmbeddedDocumentField('ImgParam'))

