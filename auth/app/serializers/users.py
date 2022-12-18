from marshmallow.validate import Length, Range
from marshmallow import fields, Schema


class UsersSchema(Schema):
    class Meta:
        fields = (
            'id',
            'username',
            'name',
            'company_id',
            'email',
            'created_on'
        )


user_schema = UsersSchema()
users_schema = UsersSchema(many=True)



class UserInputSchema(Schema):

    name = fields.String(required=True, validate=Length(max=60))
    username = fields.String(required=True, validate=Length(max=60))
    email = fields.Email(required=True, validate=Length(max=60))
    password = fields.String(required=True, validate=Length(max=60))
    company_id = fields.Integer(required=True, validate=Range(min=1))


class AuthInputSchema(Schema):
    username = fields.String(required=True, validate=Length(max=60))
    password = fields.String(required=True, validate=Length(max=60))
