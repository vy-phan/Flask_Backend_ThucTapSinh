from flask import Blueprint, jsonify, request
from ..models import db, Task  # Nhập từ thư mục models
from datetime import datetime

task_bp = Blueprint('task', __name__, url_prefix='/task')

@task_bp.route('/', methods=['GET'])
def get_all_tasks():
    try:
        tasks = Task.query.all()  # Lấy tất cả nhiệm vụ từ cơ sở dữ liệu
        return jsonify({
            'success': True,
            'data': [{
                'id': task.id,
                'code': task.code,
                'title': task.title,
                'description': task.description,
                'deadline': task.deadline.isoformat(),
                'status': task.status,
                'created_by': task.created_by,
                'created_at': task.created_at.isoformat()
            } for task in tasks]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@task_bp.route('/', methods=['POST'])
def create_task():
    try:
        # Lấy dữ liệu từ request body
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400

        # Kiểm tra các trường bắt buộc
        required_fields = ['code', 'title', 'deadline', 'created_by']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400

        # Kiểm tra định dạng deadline
        try:
            deadline = datetime.fromisoformat(data['deadline'])
        except ValueError:
            return jsonify({'success': False, 'error': 'Invalid deadline format. Use ISO format (e.g., 2025-04-21T15:30:00)'}), 400

        # Kiểm tra status hợp lệ nếu được cung cấp
        valid_statuses = ['assigned', 'in_progress', 'completed']
        status = data.get('status', 'assigned')  # Mặc định là 'assigned'
        if status not in valid_statuses:
            return jsonify({'success': False, 'error': f'Invalid status. Must be one of: {valid_statuses}'}), 400

        # Tạo task mới
        new_task = Task(
            code=data['code'],
            title=data['title'],
            description=data.get('description'),
            deadline=deadline,
            status=status,
            created_by=data['created_by']
        )

        # Thêm vào cơ sở dữ liệu
        db.session.add(new_task)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Task created successfully',
            'data': {
                'id': new_task.id,
                'code': new_task.code,
                'title': new_task.title,
                'description': new_task.description,
                'deadline': new_task.deadline.isoformat(),
                'status': new_task.status,
                'created_by': new_task.created_by,
                'created_at': new_task.created_at.isoformat()
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@task_bp.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    try:
        # Tìm task theo ID
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'success': False, 'error': 'Task not found'}), 404

        # Lấy dữ liệu từ request body
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400

        # Cập nhật các trường nếu được cung cấp
        if 'code' in data:
            task.code = data['code']
        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'deadline' in data:
            try:
                task.deadline = datetime.fromisoformat(data['deadline'])
            except ValueError:
                return jsonify({'success': False, 'error': 'Invalid deadline format. Use ISO format (e.g., 2025-04-21T15:30:00)'}), 400
        if 'status' in data:
            valid_statuses = ['assigned', 'in_progress', 'completed']
            if data['status'] not in valid_statuses:
                return jsonify({'success': False, 'error': f'Invalid status. Must be one of: {valid_statuses}'}), 400
            task.status = data['status']
        if 'created_by' in data:
            task.created_by = data['created_by']

        # Lưu thay đổi vào cơ sở dữ liệu
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Task updated successfully',
            'data': {
                'id': task.id,
                'code': task.code,
                'title': task.title,
                'description': task.description,
                'deadline': task.deadline.isoformat(),
                'status': task.status,
                'created_by': task.created_by,
                'created_at': task.created_at.isoformat()
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@task_bp.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        # Tìm task theo ID
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'success': False, 'error': 'Task not found'}), 404

        # Xóa task
        db.session.delete(task)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Task deleted successfully'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500