from flask import Blueprint, jsonify

intern_bp = Blueprint('intern', __name__ , url_prefix='/intern')

@intern_bp.route('/',methods=['GET'])
def get_all_interns():
    return jsonify({
        'success': True,
        'data': "Thông tin tất cả thực tập sinh",
    }), 200
