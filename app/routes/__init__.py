from flask import Blueprint

api_bp = Blueprint('api', __name__)

from .auth_routes import auth_bp
api_bp.register_blueprint(auth_bp)

from .intern_routes import intern_bp
api_bp.register_blueprint(intern_bp)

from .task_routes import task_bp
api_bp.register_blueprint(task_bp)
