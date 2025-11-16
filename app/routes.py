import datetime
import os
import uuid
from functools import wraps
from os.path import exists

import jwt
from flask import Blueprint, redirect, request, jsonify, current_app, send_from_directory
from multipart import file_path
from werkzeug.utils import secure_filename

from .models import db, UserModel

bp = Blueprint('routes', __name__, url_prefix='/api')


@bp.route('/')
def index():
    return redirect('/python-swagger/')


@bp.route('/users/register', methods=['POST'])
def register_user():
    data = request.get_json()
    try:

        if not data or not data.get('username') or not data.get('email') or not data.get('password'):
            return jsonify({"error": "Missing data"}), 400
        existing_user = UserModel.query.filter(
                        (UserModel.email == data.get('email')) |
                        (UserModel.username == data.get('username'))).first()
        if existing_user:
            return jsonify({"error": "Email Or username already exists"}), 400


        user = UserModel(
            username=data['username'],
            email=data['email'],
            WhatsappNumber=data.get('whatsappNumber'),
            Location=data.get('Location'),
            birthtime=data.get('Birthtime'),
            DateOfBirth =data.get('Dateofbirth'),
            password= data.get('password')

        )
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User created", "user": user.to_dict()}), 201
    except Exception as err:
        db.session.rollback()
        return jsonify({"error": str(err)}), 400



@bp.route('/users/login', methods=['POST'])
def login_user():
    data = request.get_json()
    try:
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({"error": "Missing data"}), 400
        password = data.get('password')
        user = UserModel.query.filter_by(email=data['email']).first()
        if not user or user.password != password:
            return {"error": "Invalid email or password"}, 401

        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)  # 24 hours valid
        }, current_app.config['SECRET_KEY'], algorithm='HS256')


        return jsonify({ "success": True,"message": "Login successful", "token": token }), 200
    except Exception as err:
        return jsonify({"error": str(err)}), 400


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return {"error": "Token is missing"}, 401

        # "Bearer <token>" format එකේ නම්
        if token.startswith('Bearer '):
            token = token.split(' ')[1]

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = UserModel.query.get(data['user_id'])
        except jwt.ExpiredSignatureError:
            return {"error": "Token has expired"}, 401
        except jwt.InvalidTokenError:
            return {"error": "Invalid token"}, 401

        return f(current_user, *args, **kwargs)

    return decorated

@bp.route('/users/me')
@token_required
def me(current_user):
    return current_user.to_dict()

@bp.route('/users/update', methods=['PUT'])
@token_required
def update(current_user):
    try:
        updated = False

        # Handle file upload
        if request.files.get('file') or request.files.get('Image'):
            file = request.files.get('Image')
            if file and file.filename != '':
                original_filename = secure_filename(file.filename)
                file_extension = file.filename.rsplit('.', 1)[1].lower()
                unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
                upload_folder = current_app.config['UPLOAD_FOLDER']
                os.makedirs(upload_folder, exist_ok=True)
                file_path = os.path.join(upload_folder, unique_filename)
                file.save(file_path)

                base_url = f"{request.scheme}://{request.host}"
                image_url = f"{base_url}/api/uploads/{unique_filename}"

                current_user.ProfileImage = image_url
                updated = True

        # Handle other form data
        if request.form:
            if request.form.get('email'):
                current_user.email = request.form.get('email')
                updated = True
            if request.form.get('username'):
                current_user.username = request.form.get('username')
                updated = True
            if request.form.get('whatsappNumber'):
                current_user.WhatsappNumber = request.form.get('whatsappNumber')
                updated = True
            if request.form.get('Location'):
                current_user.Location = request.form.get('Location')
                updated = True
            if request.form.get('Birthtime'):
                current_user.birthtime = request.form.get('Birthtime')
                updated = True
            if request.form.get('Dateofbirth'):
                current_user.DateOfBirth = request.form.get('Dateofbirth')
                updated = True
            if request.form.get('ID_Number'):
                current_user.NIC_Number = request.form.get('ID_Number')
                updated = True

        if updated:
            db.session.commit()
            return jsonify({
                "message": "Profile updated successfully",
                "user": current_user.to_dict()
            }), 200
        else:
            return jsonify({"error": "No data provided to update"}), 400

    except Exception as err:
        db.session.rollback()
        return jsonify({"error": str(err)}), 400



@bp.route('/uploads/<filename>')
def uploaded_file(filename):

    return send_from_directory("../uploads", filename)







