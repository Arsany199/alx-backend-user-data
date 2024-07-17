#!/usr/bin/env python3
"""model to my app file"""
from flask import Flask, jsonify, request, abort
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    """function returns json payload has a message"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users() -> str:
    """POST user and return a josn has many informations"""
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        AUTH.regester_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=["POST"])
def login() -> str:
    """create a new session for the user store it the session ID
    as a cookie with key "session_id" on the response
    and return a JSON payload of the form"""
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError:
        abort(400)
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)

    message = {"email": email, "message": "logged in"}
    res = jsonify(message)
    res.set_cookie("session_id", session_id)
    return res


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
