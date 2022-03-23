from mongoengine import Document, StringField, ListField


class Approvals(Document):
    title = StringField(required=True)
    description = StringField(required=True)
    filepath = StringField(required=True)
    member_id = StringField(required=True)
    departments = ListField(required=True)
    approval = ListField(required=True)  ###0 - Pending, 1 - Approved, 2 - Rejected
    created_date = StringField(required=True)
