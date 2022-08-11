from flask import Flask
import json

from application.handlers.routes import configure_routes

def test_base_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/api/greeting'

    response = client.get(url)
    assert response.get_data() == b'Hello, World!'
    assert response.status_code == 200

def test_health_route():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/health'

    response = client.get(url)
    assert response.status_code == 204

def test_post_route__success():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/api/test'

    mock_request_headers = {
        'authorization-sha256': '348729348723'
    }

    mock_request_data = {
        'request_id': '8437-348293486042-34895639-8974',
        'payload': {
            'name': 'tester',
            'lang': 'python'
        }
    }

    response = client.post(url, data=json.dumps(mock_request_data), headers=mock_request_headers)
    assert response.status_code == 200


def test_post_route__failure__unauthorized():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/api/test'

    mock_request_headers = {}

    mock_request_data = {
        'request_id': '8437-348293486042-34895639-8974',
        'payload': {
            'name': 'tester',
            'lang': 'python'
        }
    }

    response = client.post(url, data=json.dumps(mock_request_data), headers=mock_request_headers)
    assert response.status_code == 401


def test_post_route__failure__bad_request():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = '/api/test'

    mock_request_headers = {
        'authorization-sha256': '8437-348293486042-34895639-8974'
    }

    mock_request_data = {}

    response = client.post(url, data=json.dumps(mock_request_data), headers=mock_request_headers)
    assert response.status_code == 400
