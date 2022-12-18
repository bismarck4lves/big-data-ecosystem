from app import app
from app.utils import Response
from app.views import users


@app.route('/api/v1/', methods=['GET'])
def main():
    return Response(message="Hello").ok()


@app.route('/api/v1/sing-in/', methods=['POST'])
def sing_in():
    return users.sing_in()


@app.route('/api/v1/me/', methods=['GET'])
def me():
    return users.validate_token()


@app.route('/api/v1/sing-up/', methods=['POST'])
def sing_up():
    return users.create_user()
