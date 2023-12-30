from app import app, db, bcrypt
from flask import request, jsonify
from app.models import *
import re
from datetime import datetime

@app.route('/register',methods=['POST'])
def register_user():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password or not email:
        return jsonify({"error": "Email,Username and password are required"}), 400
    
    validation_result = validate_new_user(email=email, username=username, password=password)

    if validation_result is not None:
        return validation_result
    
    hash_password = bcrypt.generate_password_hash(password).decode('utf-8')

    user = User(
        email=email,
        username=username,
        password=hash_password,
        created_date=datetime.utcnow(),
        update_date=datetime.utcnow()
    )
    db.session.add(user)
    db.session.commit()
    

    return jsonify({"message": "User added successfully"}), 200


def validate_new_user(email,username,password):
    if not is_valid_email(email):
        return jsonify({"error": "Email is not valid"}), 400
    
    if not is_valid_password(password):
        return jsonify({"error": "Password is not valid"}), 400

    existing_user_by_email = User.query.filter_by(email=email).first()
    if existing_user_by_email:
        return jsonify({"error": "An account is already exist with this Email, please try with another one."}), 400

    existing_user_by_username = User.query.filter_by(username=username).first()
    if existing_user_by_username:
        return jsonify({"error": "That username already exists. Please choose a different one."}), 400


def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    match = re.match(pattern, email)
    return bool(match)

def is_valid_password(password):
    if len(password) < 8:
        return False
    
    if not any(char.isupper() for char in password):
        return False
    
    if not any(char.islower() for char in password):
        return False
    
    if not any(char.isdigit() for char in password):
        return False
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    
    return True


@app.route('/api',methods=['GET'])
def get_user():
    return jsonify({'message':'API working'}),200