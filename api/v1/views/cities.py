#!/usr/bin/python3
""" View for City objects that handles default RESTful API actions """
from api.v1.views import app_views
from flask import Flask, request, abort, jsonify, make_response
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """ Retrieves a list of all City objects """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    city_list = [city.to_dict() for city in state.cities]
    return jsonify(city_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_obj(city_id):
    """ Retrieves a City object"""
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """ Deletes a City object"""
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """ Creates a city """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.headers['Content-Type'] != 'application/json':
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    data = request.get_json()
    if 'name' not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)

    obj = City(**data)
    obj.state_id = state.id
    obj.save()
    return (jsonify(obj.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ Update a City object """
    if storage.get(City, city_id) is None:
        abort(404)
    if request.headers['Content-Type'] != 'application/json':
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    obj = storage.get(City, city_id)
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(obj, key, value)

    obj.save()

    return jsonify(obj.to_dict())
