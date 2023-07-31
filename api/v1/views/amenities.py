#!/usr/bin/python3
""" View for Amenity objects that handles default RESTful API actions """
from api.v1.views import app_views
from flask import Flask, request, abort, jsonify, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """ Retrieves a list of all Amenity objects """
    amenities = storage.all(Amenity).values()
    amenities_list = [amenities.to_dict() for amenities in amenities]
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenities_obj(amenity_id):
    """ Retrieves a Amenity object"""
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenities(amenity_id):
    """ Deletes a Amenity object"""
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({})


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenities():
    """ Creates a amenities """
    if request.headers['Content-Type'] != 'application/json':
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    data = request.get_json()
    if 'name' not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)

    obj = Amenity(**data)
    obj.save()
    return (jsonify(obj.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenities(amenity_id):
    """ Update a Amenity object """
    if storage.get(Amenity, amenity_id) is None:
        abort(404)
    if request.headers['Content-Type'] != 'application/json':
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    obj = storage.get(Amenity, amenity_id)
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)

    obj.save()

    return jsonify(obj.to_dict())
