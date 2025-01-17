#!/usr/bin/python3
"""states view module"""
from flask import Flask, abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def states():
    """returns list of all states"""
    if request.method == 'GET':
        states_list = []
        for state, value in storage.all(State).items():
            state = value.to_dict()
            states_list.append(state)
        return jsonify(states_list)

    if request.method == 'POST':
        # If not valid JSON, error 400
        try:
            request_data = request.get_json()
            if 'name' not in request_data:
                abort(400, "Missing name")
            newState = State(**request_data)
            newState.save()
        except Exception:
            abort(400, "Not a JSON")
        return jsonify(newState.to_dict()), 201


@app_views.route('/states/<state_id>',
                 methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def state_search(state_id):
    """returns state with id or 404"""
    state = storage.get(State, state_id)
    #  If GET
    if request.method == 'GET':
        for state, value in storage.all(State).items():
            id = (state.split(".")[1])
            if state_id == id:
                return jsonify(value.to_dict())
        abort(404)

    #  If DELETE
    if request.method == 'DELETE':
        if state is None:
            abort(404)
        storage.delete(state)
        storage.save()
        return jsonify({})

    # If PUT
    if request.method == 'PUT':
        # If not valid JSON, error 400
        if state is None:
            abort(404)
        try:
            request_data = request.get_json()
            for state, value in storage.all(State).items():
                id = (state.split(".")[1])
                if state_id == id:
                    for k in request_data.keys():
                        if k != 'id' and\
                                k != 'created_at' and k != 'updated_at':
                            setattr(value, k, request_data[k])
                    storage.save()
                return jsonify(value.to_dict())
        except Exception:
            abort(400, "Not a JSON")
        abort(404)
