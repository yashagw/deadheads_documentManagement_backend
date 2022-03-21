from mongoengine import Document, StringField, IntField, FloatField, BooleanField


class Queries(Document):
    citizen_id = StringField(required=True)
    department_id = StringField(required=True)
    title = StringField(required=True)
    description = StringField(required=True)

