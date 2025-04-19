import logging
import os
from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import Config
from logging.handlers import TimedRotatingFileHandler

# Initialize extensions
db = SQLAlchemy()

def create_app(config_class=Config):
    # Initialize Flask app
    app = Flask(__name__)
    app.config.from_object(config_class)
    

    app.config['MEDIA_FOLDER'] = 'media'
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    configure_logging(app)
    api = Api(app)
    
    # Register blueprints
    from app.routes import main
    app.register_blueprint(main, url_prefix='/api')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'message': 'Not found'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'success': False,
            'message': 'Inter server error'
        }), 500
    
    return app


# Configures the logging
def configure_logging(app):
    handler = TimedRotatingFileHandler('flask-template.log', when='midnight', interval=1, backupCount=10)
    handler.setLevel(logging.INFO) 
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
