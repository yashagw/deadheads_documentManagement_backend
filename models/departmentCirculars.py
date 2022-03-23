from mongoengine import Document, StringField, BooleanField


class DepartmentCirculars(Document):
    title = StringField(required=True)
    description = StringField(required=True)
