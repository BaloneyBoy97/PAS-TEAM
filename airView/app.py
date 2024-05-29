import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from dotenv import load_dotenv
# from authentication.auth_feature import UserRegistration, UserLogin, AdminRegistration

load_dotenv()
app = Flask(__name__)

SECRET_KEY = os.getenv('SECRET_KEY')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
MAIL_SERVER = os.getenv('MAIL_SERVER')
MAIL_PORT = int(os.getenv('MAIL_PORT'))
MAIL_USE_TLS = os.getenv('MAIL_USE_TLS') == 'True'
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

api = Api(app)
jwt = JWTManager(app)
mail = Mail(app)

# user auth feature endpoints
# api.add_resource(UserRegistration, '/register')
# api.add_resource(UserLogin, '/login')
# api.add_resource(AdminRegistration, '/admin/register')

if __name__ == '__main__':
    app.run(debug=True)