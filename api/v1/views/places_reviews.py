#!/usr/bin/python3
""" View for Review objects that handles default RESTful API actions """
from api.v1.views import app_views
from flask import Flask, request, abort, jsonify, make_response
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """ Retrieves a list of all Review objects """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    review_list = [review.to_dict() for review in place.reviews]
    return jsonify(review_list)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review_obj(review_id):
    """ Retrieves a Review object"""
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Deletes a Review object"""
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    obj.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ Creates a review """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.headers['Content-Type'] != 'application/json':
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    data = request.get_json()
    if 'user_id' not in data:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    if 'text' not in data:
        return make_response(jsonify({"error": "Missing text"}), 400)

    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    obj = Review(**data)
    obj.place_id = place.id
    obj.save()
    return (jsonify(obj.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ Update a Review object """
    if storage.get(Review, review_id) is None:
        abort(404)
    if request.headers['Content-Type'] != 'application/json':
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    obj = storage.get(Review, review_id)
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'created_at',
                       'user_id', 'place_id', 'updated_at']:
            setattr(obj, key, value)

    obj.save()

    return jsonify(obj.to_dict())
