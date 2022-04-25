from flask import jsonify


class Msg():
    def json(status=0, data=""):
        return jsonify({
            "status": status,
            "data": data
        })
