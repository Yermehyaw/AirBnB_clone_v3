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
    state_dict = state_obj.to_dict()

    return jsonify(state_dict), 200
