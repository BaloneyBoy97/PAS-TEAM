#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, send_from_directory
from flask_restful import Api
from flask_jwt_extended import JWTManager
# from flask_cors import CORS
from flask_mail import Mail
from dotenv import load_dotenv
from authentication.feature import UserRegistration, UserLogin, AdminRegistration

# Load environment variables from .env file
load_dotenv()
# Initialize Flask app
app = Flask(__name__)
# CORS(app)

# connect to HTML homepage
@app.route('/')
def serve_html():
    try:
        return send_from_directory(os.getenv('HTML_DIR', '/default/path/to/html'), 'index.html')
    except Exception as e:
        return str(e), 500

# Configure app from environment variables
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

# Initialize extensions
api = Api(app)
jwt = JWTManager(app)
mail = Mail(app)

# Add resource endpoints
api.add_resource(UserRegistration, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(AdminRegistration, '/admin/register')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
