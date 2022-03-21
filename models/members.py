from mongoengine import Document, StringField, IntField, FloatField, BooleanField


class Members(Document):
    organisation_id = StringField(required=True)
    department_id = StringField(required=True)
    name = StringField(required=True)
    email = StringField(required=True)
    password = StringField(required=True)