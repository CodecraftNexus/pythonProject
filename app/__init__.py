import os
from flask import Flask, send_from_directory
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
    os.getenv('DB_USER'),
    os.getenv('DB_PASS'),
    os.getenv('DB_HOST', 'localhost'),
    os.getenv('DB_PORT', '3306'),
    os.getenv('DB_NAME')
)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = False

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    db.init_app(app)



    @app.route('/apispec.json')
    def apispec():
        return send_from_directory('../static', 'swagger.json')

    from app.utils.swagger import setup_swagger
    setup_swagger(app)

    from .routes import bp
    app.register_blueprint(bp)

    return app



