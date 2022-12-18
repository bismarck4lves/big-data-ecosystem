from flask import jsonify


class Response:

    def __init__(
        self,
        data=None,
        message="",
        detail="",
    ) -> None:
        self.data = data
        self.detail = detail
        self.message = message

    def ok(self):
        return jsonify(self.__prepare_response()), 200

    def unAuthorized(self):
        return jsonify(self.__prepare_response()), 401

    def not_found(self):
        return jsonify(self.__prepare_response()), 404

    def created(self):
        return jsonify(self.__prepare_response()), 201

    def error(self):
        return jsonify(self.__prepare_response()), 500

    def __prepare_response(self):
        res = {}
        if self.message:
            res.update({"message": self.message})
        if self.data:
            res.update({"data": self.data})
        if self.detail:
            res.update({"detail": self.detail})
        return res
