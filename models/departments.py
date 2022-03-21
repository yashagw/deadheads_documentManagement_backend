from mongoengine import Document, StringField, IntField, FloatField, BooleanField


class Departments(Document):
    organisation_id = StringField(required=True)
    name = StringField(required=True)
    tagline = StringField()
    head_name = StringField(required=True)
    email = StringField(required=True)
    password = StringField(required=True)