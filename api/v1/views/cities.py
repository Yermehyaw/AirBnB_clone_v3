#!/usr/bin/python3
"""
Define Blueprint route/view funcs to manipulate State() objects in storage

IMPORTS: abort, app_views, jsonify, request, State, storage
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.state import State


# The full url is '/api/v1/states', '/ap1/v1' is the defined url_prefix
@app_views.route(
    '/states/<state_id>/cities',
    methods=['GET'],
    strict_slashes=False
)
def all_cities(state_id):
    """Return list of all city objects in JSON"""
    storage.reload()  # load prev saved objects from db or json file
    state_obj = storage.get(State, state_id)
    if not state_obj:
        storage.close()
        abort(404)

    city_obj_list = state_obj.cities
    for obj in city_obj_list:
        obj = obj.to_dict()
    storage.close()
    return jsonify(city_obj_list), 200


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def spec_city(city_id):
    """Return a specified state object by its unique id"""
    storage.reload()
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        storage.close()
        abort(404)
    city_obj_dict = city_obj.to_dict()

    storage.close()
    return jsonify(city_obj_dict), 200


@app_views.route(
    '/cities/<city_id>',
    methods=['DELETE'],
    strict_slashes=False
)
def delete_city(city_id):
    """Delete a specified city object in storage"""
    storage.reload()
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        storage.close()
        abort(404)
    else:
        storage.delete(city_obj)
        storage.close()
        return jsonify({}), 200


@app_views.route(
    '/states/<state_id>/cities',
    methods=['POST'],
    strict_slashes=False
)
def create_city():
    """Create a new city object in storage"""
    if not request.is_json:
        abort(400, 'Not a JSON')
    if 'name' not in request.json:
        abort(400, 'Missing Name')
    storage.reload()
    state_obj = storage.get(State, state_id)
    if not state_obj:
        storage.close()
        abort(404)
    req_city = request.get_json()
    new_city = City()
    new_city.name = req_city['name']

    storage.new(new_city)
    storage.save()
    storage.close()

    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Update a city object"""
    storage.reload()

    city_obj = storage.get(City, city_id)
    if not city_obj:
        storage.close()
        abort(404)
    if not request.is_json:
        storage.close()
        abort(404. 'Not a JSON')

    update_city = request.get_json()  # convert request from client to json
    for key in update_city:
        if key == 'name':
            city_obj.name = update_city[key]

    storage.delete(city_obj)  # delete previous object
    storage.new(city_obj)  # add the updated version of the object
    storage.save()
    storage.close()

    return jsonify(city_obj.to_dict()), 200
