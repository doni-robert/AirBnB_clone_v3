#!/usr/bin/python3
""" View for State objects that handles default RESTful API actions """
from api.v1.views import app_views
from flask import Flask, request, abort, jsonify, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """ Retrieves a list of all State objects """
    states = storage.all(State).values()
    state_list = [state.to_dict() for state in states]
    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_obj(state_id):
    """ Retrieves a State object"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ Deletes a State object"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    obj.delete()
    del obj
    return jsonify({})


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ Creates a state """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    data = request.get_json()
    if 'name' not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)

    obj = State(**data)
    obj.save()
    return (jsonify(obj.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ Update a State object """
    if storage.get(State, state_id) is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    obj = storage.get(State, state_id)
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)

    obj.save()

    return jsonify(obj.to_dict())
