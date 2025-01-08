import os

import dns.resolver
from flask import Flask, render_template, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['8.8.8.8']

from routes import auth_bp, schedule_bp, task_bp

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template('index.html', url=request.url)

@app.route("/bg-sync")
def bg_sync():
    print("Background sync")
    return "Background sync"

@app.route("/periodic")
def periodic():
    print("Periodic")
    return "Periodic"

SWAGGER_URL = "/docs"
API_URL = "/static/swagger/config.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'PlannerTNP API'
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(schedule_bp, url_prefix='/schedule')
app.register_blueprint(task_bp, url_prefix='/task')

app_port = int(os.getenv('BACKEND_PORT', 1234))

if __name__ == '__main__':
    app.run(debug=True, port=app_port)