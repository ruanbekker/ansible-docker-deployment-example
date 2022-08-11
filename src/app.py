# credit: https://github.com/aaronjolson/flask-pytest-example
from flask import Flask, render_template
from handlers.routes import configure_routes

app = Flask(__name__)
configure_routes(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
