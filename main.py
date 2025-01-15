import os
import time
import dns.resolver
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
import endpoints.get_wtt_excel as wtt_excel

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

@app.route("/options", methods=["GET"])
def get_programs():
    driver, wait = wtt_excel.init_driver()
    try:
        driver.get("https://www.wise-tt.com/wtt_um_feri/")
        programs = wtt_excel.get_select_options(wait, div_index=2)[1]
        return jsonify({"programs": programs })
    finally:
        driver.quit()

@app.route("/options", methods=["POST"])
def get_options():
    data = request.json
    program_index = data.get("program_index")

    if program_index is None:
        return jsonify({"error": "Missing program index"}), 400

    driver, wait = wtt_excel.init_driver()
    try:
        driver.get("https://www.wise-tt.com/wtt_um_feri/")

        # Select program
        wtt_excel.select_option(wait, div_index=2, option_index=program_index)
        time.sleep(1)  # Allow dependent options to load

        # Fetch years and modules
        years = wtt_excel.get_select_options(wait, div_index=3)[1]
        modules = wtt_excel.get_select_options(wait, div_index=4)[1]

        return jsonify({"years": years, "modules": modules})
    finally:
        driver.quit()

@app.route("/download", methods=["POST"])
def download():
    data = request.json
    program_index = data.get("program_index")
    year_index = data.get("year_index")
    module_index = data.get("module_index")

    if program_index is None or year_index is None or module_index is None:
        return jsonify({"error": "Missing program, year, or module index"}), 400

    driver, wait = wtt_excel.init_driver()
    try:
        downloaded_files = wtt_excel.download_excel(driver, wait, program_index, year_index, module_index)
        return jsonify({"downloaded_files": downloaded_files})
    finally:
        driver.quit()

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