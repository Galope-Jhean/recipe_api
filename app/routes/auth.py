from flask import Blueprint, request, jsonify
from app.models import User
from app.extensions import db
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()

        if not data.get("username") or not data.get("password"):
            return jsonify({"error": "Missing required fields"}), 400
        if User.query.filter_by(username=data["username"]).first():
            return jsonify({"error": "Username already exists"})

        new_user = User(username=data["username"])
        new_user.set_password(data["password"])

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registration was successful"})

    except Exception:
        return jsonify({"error": "Registration failed"}), 500


@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        if not data.get("username") or not data.get("password"):
            return jsonify({"error": "Missing required fields"}), 400

        user = User.query.filter_by(username=data["username"]).first()

        if user is None or not user.check_password(data.get("password")):
            return jsonify({"error": "Invalid Credentials"}), 400

        access_token = create_access_token(identity=str(user.id))

        return jsonify({"access_token": access_token}), 200

    except Exception:
        return (
            jsonify({"error": "Something went wrong while logging in"}),
            500,
        )
