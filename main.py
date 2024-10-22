from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from controllers.project_bp import project_bp
from controllers.idea_bp import idea_bp
from controllers.user_bp import user_bp
port=5551

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/users')

if __name__ == '__main__':
    app.run(debug=True, port=port)