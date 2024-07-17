#!/usr/bin/env python3
"""model to my app file"""
from flask import Flask, jsonify, request, abort, redirect
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


@app.route("/sessions", methods=["POST"])
def login() -> str:
    """create a new session for the user store it the session ID
    as a cookie with key "session_id" on the response
    and return a JSON payload of the form"""
    try:
        email = request.form["email"]
        password = request.form["password"]
    except KeyError:
        abort(400)
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)

    message = {"email": email, "message": "logged in"}
    res = jsonify(message)
    res.set_cookie("session_id", session_id)
    return (res)


@app.route("/sessions", methods=["DELETE"])
def logout() -> str:
    """find user with session id if exist delete it and redirect to GET /
    if not found respond with 403 http"""
    session_id = request.cookies.get("session_id", None)

    if session_id is None:
        abort(403)

    myuser = AUTH.get_user_from_session_id(session_id)
    if myuser is None:
        abort(403)

    AUTH.destroy_session(myuser.id)

    return redirect('/')


@app.route("/profile", methods=["GET"])
def profile() -> str:
    """if the profile exist respond with 200 http"""
    session_id = request.cookies.get("session_id", None)

    if session_id is None:
        abort(403)

    myuser = AUTH.get_user_from_session_id(session_id)
    if myuser is None:
        abort(403)

    message = {"email": myuser.email}
    return jsonify(message), 200


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token() -> str:
    """if the email not regestered respond with 403 otherwise 200"""
    email = request.form.get("email")
    try:
        new_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "reset_token": new_token})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
