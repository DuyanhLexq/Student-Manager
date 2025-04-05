from flask import request,jsonify
from flask_jwt_extended import create_access_token,get_jwt_identity


def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Kiểm tra thông tin người dùng từ DB (giả sử hợp lệ)
    if username == 'test' and password == '123':
        access_token = create_access_token(identity=username)
        return jsonify(token=access_token), 200
    return jsonify({"msg": "Sai thông tin"}), 401

def user_info():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200