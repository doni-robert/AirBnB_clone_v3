#!/usr/bin/python3
""" View for Place objects that handles default RESTful API actions """
from api.v1.views import app_views
from flask import Flask, request, abort, jsonify, make_response
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """ Retrieves a list of all Place objects """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    place_list = [place.to_dict() for place in city.places]
    return jsonify(place_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place_obj(place_id):
    """ Retrieves a Place object"""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Deletes a Place object"""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ Creates a place """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.headers['Content-Type'] != 'application/json':
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    data = request.get_json()
    if 'name' not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)
    if "user_id" not in data():
        return jsonify({"error": "Missing user_id"}), 400

    data['city_id'] = city_id
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)

    obj = Place(**data)
    obj.save()
    return (jsonify(obj.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Update a Place object """
    if storage.get(Place, place_id) is None:
        abort(404)
    if request.headers['Content-Type'] != 'application/json':
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    obj = storage.get(Place, place_id)
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(obj, key, value)

    obj.save()

    return jsonify(obj.to_dict())
