from mongoengine import Document, StringField, IntField, FloatField, BooleanField


class Organisations(Document):
    name = StringField(required=True)
    tagline = StringField()
    director_name = StringField(required=True)
    city = StringField()
    state = StringField()
    pincode = IntField()
    logo = StringField()
    banner = StringField()
    email = StringField()
    password = StringField()

