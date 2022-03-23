from mongoengine import Document, StringField, BooleanField


class MemberCirculars(Document):
    title = StringField(required=True)
    description = StringField(required=True)
    department_id = StringField(required=True) ##All -> every member, id from db so show only the members of this id
