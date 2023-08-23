#!/usr/bin/python3
"""states view module"""
from flask import Flask, abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.state import State

@app_views.route('/states',methods = ['GET', 'POST'], strict_slashes=False)
def states():
    """returns list of all states"""
    if request.method == 'GET':
      states_list = []
      for state, value in storage.all(State).items():
          state = value.to_dict()
          states_list.append(state)
      return (states_list)

    if request.method == 'POST':
      # If not valid JSON, error 400
      try:
        request_data = request.get_json()
      except:
         abort(400, "Not a JSON")
      if 'name' not in request_data:
         abort(400, "Missing name")
      fff = State(**request_data)
      
      return fff.to_dict()

@app_views.route('/states/<state_id>', methods=['GET', 'DELETE'], strict_slashes=False)
def state_search(state_id):
    """returns state with id or 404"""

    #  If GET
    if request.method == 'GET':
      for state, value in storage.all(State).items():
          id = (state.split(".")[1])
          if state_id == id:
              return value.to_dict()
      abort(404)

    #  If DELETE
    if request.method == 'DELETE':
      state = storage.get(State, state_id)
      if state is not None:
        storage.delete(state)
        storage.save()
        return jsonify({})
      else:
         abort(404) 
