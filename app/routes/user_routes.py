from flask import Blueprint, jsonify

user_bp = Blueprint('user', __name__ , url_prefix='/user')

@user_bp.route('/',methods=['GET'])
def get_all_users():
    return jsonify({
        'success': True,
        'data': "Thông tin tất cả thực tập sinh",
    }), 200
