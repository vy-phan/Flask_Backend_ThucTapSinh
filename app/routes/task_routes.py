from flask import Blueprint, jsonify, request
from ..services.task_service import TaskService
from ..models import db

task_bp = Blueprint('task', __name__, url_prefix='/task')

@task_bp.route('/', methods=['GET'])
def get_all_tasks():
    try:
        service = TaskService()
        tasks = service.get_all_tasks()
        return jsonify({'success': True, 'data': tasks}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@task_bp.route('/', methods=['POST'])
def create_task():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400

        service = TaskService()
        new_task = service.create_task(data)
        return jsonify({
            'success': True,
            'message': 'Task created successfully',
            'data': new_task
        }), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@task_bp.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400

        service = TaskService()
        updated_task = service.update_task(task_id, data)
        return jsonify({
            'success': True,
            'message': 'Task updated successfully',
            'data': updated_task
        }), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@task_bp.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        service = TaskService()
        service.delete_task(task_id)
        return jsonify({
            'success': True,
            'message': 'Task deleted successfully'
        }), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500