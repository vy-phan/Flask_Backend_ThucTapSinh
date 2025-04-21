from flask import Blueprint ,jsonify

task_bp = Blueprint('task', __name__ , url_prefix='/task')

@task_bp.route('/',methods=['GET'])
def get_all_tasks():
    return jsonify({
        'success': True,
        'data': "Thông tin tất cả công việc",
    }), 200
