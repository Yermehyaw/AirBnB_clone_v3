#!/usr/bin/python3
"""
Define Blueprint route/view funcs to manipulate State() objects in storage

IMPORTS: abort, app_views, jsonify, request, State, storage
"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models.states import State
from models.storage import storage

# The full url is '/api/v1/states', '/ap1/v1' is the defined url_prefix
@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_staes():
    """Return list of all state objects in JSON"""
    all_state_list = []
    all_state_obj = storage.all(State)
    for obj in all_state_obj:
        all_state_list.append(obj.to_dict())

    return jsonify(all_state_list), 200

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def spec_state(state_id):
    """Return a specified state object by its unique id"""
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    state_obj_dict = state_obj.to_dict()

    return jsonify(state_obj_dict), 200

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Delete a specified state object in storage"""
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    else:
        storage.delete(state_obj)
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

    storage.new(new_state)
    storage.save()

    return jsonify(new_state.to_dict()), 201
