#!/usr/bin/env python3
"""Flask application
"""
from flask import Flask, jsonify, request, abort, make_response
from auth import Auth


app = Flask(__name__)
auth = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def hello() -> str:
    """GET /
    Return:
      - a welcome message
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user() -> str:
    """POST /users
    JSON body:
      - email: the user's email
      - password: the user's password
    Return:
      - a JSON response with the new user's email
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = auth.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return make_response(
          jsonify({"message": "email already registered"}), 400)


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """POST /sessions
    JSON body:
      - email: the user's email
      - password: the user's password
    Return:
      - a JSON response with the user's email and a message
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not auth.valid_login(email, password):
        abort(401)

    session_id = auth.create_session(email)
    if not session_id:
        abort(401)

    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)

    return response

@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """DELETE /sessions
    JSON body:
      - session_id: the session_id
    Return:
      - an empty JSON response
    """
    session_id = request.cookies.get('session_id')
    user = auth.get_user_from_session_id(session_id)

    if not user:
        abort(403)

    auth.destroy_session(user.id)

    return jsonify({}), 200

@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """GET /profile
    JSON body:
      - session_id: the session_id
    Return:
      - a JSON response with the user's email
    """
    session_id = request.cookies.get('session_id')
    user = auth.get_user_from_session_id(session_id)

    if not user:
        abort(403)

    return jsonify({"email": user.email}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
