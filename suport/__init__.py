import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()


def flask_app():
    app = Flask(__name__)  
    app.config['SECRET_KEY'] = 'secretkey'
    if os.environ.get('DATABASE_URL'):
        uri = os.environ.get('DATABASE_URL')
        if uri.startswith("postgres://"):
            uri = uri.replace("postgres://", "postgresql://", 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = uri
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/test'
    db.init_app(app)
    

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Review
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
  
def create_database(app):
    if not path.exists('suport/'):
        db.create_all(app=app)
        print('Created Database!')