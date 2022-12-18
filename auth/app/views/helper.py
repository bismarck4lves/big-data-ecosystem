import datetime
from functools import wraps
from app import app
from flask import request, jsonify
from .users import user_by_username
from app.utils import Response
import jwt
from werkzeug.security import check_password_hash


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return Response(
                message="token is missing",
                data=[]
            ).unAuthorized()
        
        try:
            data = jwt.decode(
                token,
                app.config['SECRET_KEY']
            )
            current_user = user_by_username(username=data['username'])

        except:
            return Response(
                message="token is invalid or expired",
                data=[]
            ).unAuthorized()
        return f(current_user, *args, **kwargs)
    return decorated


def auth():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({
            'message': 'could not verify',
            'WWW-Authenticate': 'Basic auth="Login required"'
        }), 401
    user = user_by_username(auth.username)
    if not user:
        return jsonify({
            'message': 'user not found',
            'data': []
        }), 401

    if user and check_password_hash(user.password, auth.password):
        token = jwt.encode({
            'username': user.username,
            'exp': datetime.datetime.now() + datetime.timedelta(hours=12)
            },
            app.config['SECRET_KEY']
        )
        return jsonify({
            'message': 'Validated successfully',
            'token': token.decode('UTF-8'),
            'exp': datetime.datetime.now() + datetime.timedelta(hours=12)
        })

    return jsonify({
        'message': 'could not verify',
        'WWW-Authenticate': 'Basic auth="Login required"'
    }), 401
