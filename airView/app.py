#!/usr/bin/env python3
import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_mail import flask_mail
from dotenv import load_dotenv
# from authentication.auth_feature import UserRegistration, UserLogin, AdminRegistration

app = Flask(__main__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

api = Api(app)
jwt = JWTManager(app)
mail = Mail(app)

# api.add_resources(UserRegistration, '/register')
# api.add_resources(UserLogin, '/login')
# api.add_resources(AdminREgistration, '/admin/register')

if __name__ == '__main__':
    app.run(debug=True)

