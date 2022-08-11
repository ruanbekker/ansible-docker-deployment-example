from flask import request, render_template
from os import environ 
from socket import gethostname
import json

def configure_routes(app):

    @app.route('/')
    def root():
        hostname = gethostname()
        return render_template(
            'index.html', 
            app_title = environ['APP_TITLE'],
            environment = environ['APP_ENV'], 
            hostname = hostname,
            python_version = environ['PYTHON_VERSION']
        )

    @app.route('/api/greeting')
    def hello_world():
        return 'Hello, World!'

    @app.route('/api/test', methods=['POST'])
    def receive_post():
        headers = request.headers

        auth_token = headers.get('authorization-sha256')
        if not auth_token:
            return 'Unauthorized', 401

        data_string = request.get_data()
        data = json.loads(data_string)

        request_id = data.get('request_id')
        payload = data.get('payload')

        if request_id and payload:
            return 'Ok', 200
        else:
            return 'Bad Request', 400

    @app.route('/health')
    def health():
        return ('', 204)
