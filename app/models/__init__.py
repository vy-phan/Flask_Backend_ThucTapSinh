from flask_sqlalchemy import SQLAlchemy

from app import db  # Import db từ app/__init__.py

from .task import Task  # Nhập mô hình Task
from .user import User

from .role import UserRole