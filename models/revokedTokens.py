from flask_mongoengine import Document
from mongoengine import StringField


class RevokedTokens(Document):
    jti = StringField()
