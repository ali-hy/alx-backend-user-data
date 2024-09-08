#!/usr/bin/env python3
""" Module of Index views
"""
from typing import Type
from flask import jsonify, abort, Request
from api.v1.views import app_views

@app_views.errorhandler(401)
def unauthorizedHandler(error: Type[Exception]) -> str:
    """ Return a 401 error"""
    return jsonify({"error": "Unauthorized"}), 401

@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def unauthorized() -> str:
    """ GET /api/v1/unauthorized
    Return:
      - 401 error
    """
    abort(401)

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """ GET /api/v1/status
    Return:
      - the status of the API
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """ GET /api/v1/stats
    Return:
      - the number of each objects
    """
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)
