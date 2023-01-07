from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "products.db"

def config_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'intella'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    from .views import views
    
    app.register_blueprint(views, url_prefix='/')
    
    # Setup for database
    with app.app_context():
        db.create_all()
    
    return app
