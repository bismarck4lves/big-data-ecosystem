import jwt
import datetime
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from app import db, app
from ..models.users import Users
from ..utils.http import Response
from ..serializers.users import user_schema, UserInputSchema, AuthInputSchema


secret = "C58633"
def create_user():

    errors = UserInputSchema().validate(data=request.json)
    if errors:
        return Response(message="invalid fields", data=errors).error()

    username = request.json["username"]
    password = request.json["password"]
    name = request.json["name"]
    email = request.json["email"]
    company_id = request.json["company_id"]

    user = user_by_username(username)
    if user:
        result = user_schema.dump(user)
        return Response(message="user already exists", data={}).error()

    pass_hash = generate_password_hash(password)
    user = Users(username, pass_hash, name, email, company_id)

    try:
        db.session.add(user)
        db.session.commit()
        result = user_schema.dump(user)
        return Response(
            message="successfully registered",
            data=result
        ).created()

    except Exception:
        return Response(message="unable to create").error()


def sing_in():
    errors = AuthInputSchema().validate(data=request.json)

    username = request.json["username"]
    password = request.json["password"]

    if errors:
        return Response(message="could not verify").unAuthorized()

    user = user_by_username(username)
    if not user:

        return Response(message="user not found").unAuthorized()

    if user and check_password_hash(user.password, password):
        token = jwt.encode(
            {
                "username": user.username,
                "exp": datetime.datetime.now() + datetime.timedelta(hours=12),
            },
            secret,
            algorithm="HS256"
        )
        return Response(
            message="Validated successfully",
            data={
                "token": token,
                "exp": datetime.datetime.now() + datetime.timedelta(hours=12),
            },
        ).ok()

    return Response(message="could not verify").unAuthorized()


def validate_token():
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1]

    if not token:
        return Response(
            message="token is missing",
            data=[]
        ).unAuthorized()
    
    try:
        data = jwt.decode(
            token,
            secret,
            algorithms=["HS256"]
        )
        current_user = user_by_username(username=data['username'])
        result = user_schema.dump(current_user)
        return Response(data=result).ok()

    except Exception as e:
        print(e)
        return Response(
            message="error",
            data=[]
        ).unAuthorized()


def user_by_username(username):
    try:
        return Users.query.filter(Users.username == username).one()
    except Exception:
        return None
