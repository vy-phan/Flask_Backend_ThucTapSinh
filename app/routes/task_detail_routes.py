from flask import Blueprint, jsonify, request
from ..models import db, Task_Detail, Task  # Nhập từ thư mục models
from datetime import datetime

task_detail_bp = Blueprint('task_detail', __name__, url_prefix='/task_detail')
#lấy dữ liệu task_detail theo task_id
task_detail_bp.route('/<int:task_id>', methods=['GET'])
def get_task_detail(task_id):
    #Lấy toàn bộ task_detail từ database
    task_details = Task_Detail.query.filter_by(task_id=task_id).all()
    if not task_details:
        return jsonify({"message": "No task details found"}), 404
    task_detail_list = []
    for task in task_details:
        task_detail_list.append({
            "id": task.id,
            "task_id": task.task_id,
            "name": task.name,
            "description": task.description,
            "created_at": task.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": task.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        })
    return jsonify(task_detail_list), 200


#Hiển thị toàn bộ dữ liệu bảng task_detail ko theo task_id
@task_detail_bp.route('/', methods=['GET'])
def get_all_task_details():
    #Lấy toàn bộ task_detail từ database
    task_details = Task_Detail.query.all()
    if not task_details:
        return jsonify({"message": "No task details found"}), 404
    task_detail_list = []
    for task in task_details:
        task_detail_list.append({
            "id": task.id,
            "task_id": task.task_id,
            "name": task.name,
            "description": task.description,
            "created_at": task.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": task.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        })
    return jsonify(task_detail_list), 200

#thêm dữ liệu task_detail
@task_detail_bp.route('/add', methods=['POST'])
def add_task_detail():
    try:
        data = request.get_json()

        task_id = data.get('task_id')
        title = data.get('title')
        description = data.get('description', '')
        status = 'Đã giao'

        # Validate input
        if not all([task_id, title, status]):
            return jsonify({'error': 'Các trường task_id, title và status là bắt buộc'}), 400



        # Kiểm tra xem task có tồn tại không
        print('tìm id')
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': f'Task với id {task_id} không tồn tại'}), 404
        print('tìm id thành công')
        # Tạo mới task_detail
        new_detail = Task_Detail(
            task_id=task_id,
            title=title,
            description=description,
            status=status,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        print('tạo mới task_detail thành công')
        db.session.add(new_detail)
        db.session.commit()

        return jsonify({
            'message': 'Tạo task detail thành công',
            'task_detail': {
                'id': new_detail.id,
                'title': new_detail.title,
                'status': new_detail.status,
                'task_id': new_detail.task_id,
                'task_title': task.title
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    

#cập nhật dữ liệu task_detail
@task_detail_bp.route('/update/<int:task_detail_id>', methods=['PUT'])
def update_task_detail(task_detail_id):
    try:
        data = request.get_json()
        task_detail_record = Task_Detail.query.get(task_detail_id)

        if not task_detail_record:
            return jsonify({'error': 'Task detail không tồn tại'}), 404

        # Cập nhật các trường cần thiết
        task_detail_record.title = data.get('title', task_detail_record.title)
        task_detail_record.description = data.get('description', task_detail_record.description)
        task_detail_record.status = data.get('status', task_detail_record.status)
        task_detail_record.updated_at = datetime.utcnow()

        db.session.commit()

        return jsonify({
            'message': 'Cập nhật thành công',
            'task_detail': {
                'id': task_detail_record.id,
                'title': task_detail_record.title,
                'status': task_detail_record.status,
                'task_id': task_detail_record.task_id
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
    
#xóa dữ liệu task_detail
@task_detail_bp.route('/delete/<int:task_detail_id>', methods=['DELETE'])
def delete_task_detail(task_detail_id):
    try:
        task_detail_record = Task_Detail.query.get(task_detail_id)

        if not task_detail_record:
            return jsonify({'error': 'Task detail không tồn tại'}), 404

        db.session.delete(task_detail_record)
        db.session.commit()

        return jsonify({'message': 'Xóa thành công'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500