#!/usr/bin/python3
"""
Define Blueprint route/view funcs to manipulate State() objects in storage

IMPORTS: abort, app_views, jsonify, request, State, storage
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.state import State


# The full url is '/api/v1/states', '/ap1/v1' is the defined url_prefix
@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """Return list of all state objects in JSON"""
    storage.reload()  # load prev saved objects from db or json file
    all_state_list = []
    all_state_obj = storage.all(State)
    for obj in all_state_obj:
        all_state_list.append(obj.to_dict())

    storage.close()
    return jsonify(all_state_list), 200

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def spec_state(state_id):
    """Return a specified state object by its unique id"""
    storage.reload()
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        storage.close()
        abort(404)
    state_obj_dict = state_obj.to_dict()

    storage.close()
    return jsonify(state_obj_dict), 200

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Delete a specified state object in storage"""
    storage.reload()
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        storage.close()
        abort(404)
    else:
        storage.delete(state_obj)
        storage.close()
        return jsonify({}), 200

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Create a new state object in storage"""
    if not request.is_json:
        abort(400, 'Not a JSON')
    if 'name' not in request.json:
        abort(400, 'Missing Name')
    req_state = request.get_json()
    new_state = State()
    new-state.name = req_state['name']

    storage.reload()
    storage.new(new_state)
    storage.save()
    storage.close()

    return jsonify(new_state.to_dict()), 201

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Update a state object"""
    storage.reload()

    state_obj = storage.get(State, state_id)
    if not state_obj:
        storage.close()
        abort(404)
    if not request.is_json:
        storage.close()
        abort(404. 'Not a JSON')

    update_state = request.get_json()  # convert request from client to json
    for key in update_state:
        if key == 'name':
            state_obj.name = update_state[key]

    storage.delete(state_obj)  # delete previous object
    storage.new(state_obj)  # add the updated version of the object
    storage.save()
    storage.close()

    return jsonify(state_obj.to_dict()), 200
