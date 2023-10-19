from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()

def flask_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'project3'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/test'
    db.init_app(app)
    
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    
    
    from .models import User, Note
    
    
    return app

def create_database(app):
    if not path.exists('suport/'):
        db.create_all(app=app)
        print('Created Database!')