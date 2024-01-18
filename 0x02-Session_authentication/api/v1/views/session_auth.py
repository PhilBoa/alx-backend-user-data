#!/usr/bin/env python3
"""
SessionAuth views module
"""
from flask import request, jsonify
from api.v1.views import app_views
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """ Session authentication login route """
    email = request.form.get("email")
    password = request.form.get("password")

    if email is None or email == "":
        return jsonify({"error": "email missing"}), 400

    if password is None or password == "":
        return jsonify({"error": "password missing"}), 400

    user = User.search({"email": email})
    if not user or user == []:
        return jsonify({"error": "no user found for this email"}), 404

    for usr in user:
        if usr.is_valid_password(password):
            from api.v1.app import auth
            session_id = auth.create_session(usr.id)
            response = jsonify(usr.to_json())
            session_name = os.getenv('SESSION_NAME')
            response.set_cookie(session_name, session_id)
            return response
    return jsonify({"error": "wrong password"}), 401


@app_views.route(
        '/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """Logout a user session"""
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
