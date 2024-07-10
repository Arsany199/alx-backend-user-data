#!/usr/bin/env python3
""" Module of Session authentication views
"""
from models.user import User
from os import getenv
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """function returns the login information"""
    email = request.form.get('email')

    if not email:
        return (jsonify({"error": "email missing"}), 400)

    password = request.form.get('password')

    if not password:
        return (jsonify({"error": "password missing"}), 400)

    try:
        found_users = User.search({'email': email})
    except Exception:
        return (jsonify({"error": "no user found for this email"}), 404)

    if not found_users:
        return (jsonify({"error": "no user found for this email"}), 404)

    for u in found_users:
        if not u.is_valid_password(password):
            return (jsonify({"error": "wrong password"}), 401)

    from api.v1.app import auth

    u = found_users[0]
    session_id = auth.create_session(u.id)

    SESSION_NAME = getenv("SESSION_NAME")

    response = jsonify(user.to_json())
    response.set_cookie(SESSION_NAME, session_id)

    return (response)


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout():
    """function to logout and return empty directory"""
    from api.v1.app import auth

    dele = auth.destroy_session(request)

    if not dele:
        abort(404)

    return (jsonify({}), 200)
