#!/usr/bin/python3
"""
Contains the general endpoints
"""
from models import storage
from flask import Flask, jsonify
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def status():
    """ Returns the status """
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False, methods=['GET'])
def count():
    """ Retrieves the count of the objects """
    return jsonify({"amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")})
