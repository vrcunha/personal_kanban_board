from http import HTTPStatus
from flask import Flask, jsonify
from src.utils.setting import setting

def create_app():

    app = Flask(__name__)

    @app.route('/', methods=['GET'], strict_slashes=False)
    def health_check():
        resp = {
            'app_name': setting.APP_NAME,
            'app_version': setting.APP_VERSION
        }
        return jsonify(resp), HTTPStatus.OK

    return app
