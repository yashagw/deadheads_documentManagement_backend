from mongoengine import Document, StringField


class Citizens(Document):
    name = StringField(required=True)
    email = StringField(required=True)
    password = StringField(required=True)