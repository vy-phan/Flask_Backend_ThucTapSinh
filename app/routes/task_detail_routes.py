from flask import Blueprint, request, jsonify
from app.services.task_detail_services import(
    fetch_task_details_by_task_id,
    fetch_all_task_details,
    create_task_detail,
    modify_task_detail,
    remove_task_detail
)

task_detail_bp = Blueprint('task_detail', __name__, url_prefix='/task_detail')


@task_detail_bp.route('/<int:task_id>', methods=['GET'])
def get_task_detail(task_id):
    task_details = fetch_task_details_by_task_id(task_id)
    if not task_details:
        return jsonify({"message": "No task details found"}), 404

    return jsonify([
        {
            "id": t.id,
            "task_id": t.task_id,
            "title": t.title,
            "description": t.description,
            "created_at": t.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": t.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        } for t in task_details
    ]), 200


@task_detail_bp.route('/', methods=['GET'])
def get_all_task_details():
    task_details = fetch_all_task_details()
    if not task_details:
        return jsonify({"message": "No task details found"}), 404

    return jsonify([
        {
            "id": t.id,
            "task_id": t.task_id,
            "title": t.title,
            "description": t.description,
            "created_at": t.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": t.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        } for t in task_details
    ]), 200


@task_detail_bp.route('/add', methods=['POST'])
def add_task_detail():
    try:
        data = request.get_json()
        new_detail, task_title = create_task_detail(data)

        return jsonify({
            'message': 'Tạo task detail thành công',
            'task_detail': {
                'id': new_detail.id,
                'title': new_detail.title,
                'status': new_detail.status,
                'task_id': new_detail.task_id,
                'task_title': task_title
            }
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except LookupError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@task_detail_bp.route('/update/<int:task_detail_id>', methods=['PUT'])
def update_task_detail(task_detail_id):
    try:
        data = request.get_json()
        updated = modify_task_detail(task_detail_id, data)
        return jsonify({
            'message': 'Cập nhật thành công',
            'task_detail': {
                'id': updated.id,
                'title': updated.title,
                'status': updated.status,
                'task_id': updated.task_id
            }
        }), 200
    except LookupError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@task_detail_bp.route('/delete/<int:task_detail_id>', methods=['DELETE'])
def delete_task_detail(task_detail_id):
    try:
        remove_task_detail(task_detail_id)
        return jsonify({'message': 'Xóa thành công'}), 200
    except LookupError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
