from flask import Blueprint, jsonify

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Здесь может быть логика проверки авторизации
    return jsonify({"message": "Login successful"}), 200

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # Здесь может быть логика регистрации пользователя
    return jsonify({"message": "Registration successful"}), 200
