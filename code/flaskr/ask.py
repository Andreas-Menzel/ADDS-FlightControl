import functools

from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

# Import own files
from functions_collection import *


bp = Blueprint('ask', __name__, url_prefix='/ask')


@bp.route('/get_drone_info')
def get_drone_info():
    response = get_response_template(response_data=True)

    drone_id = request.values.get('drone_id')
    
    # Check if all required values were given
    response = check_argument_not_null(response, drone_id, 'drone_id')
    
    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    db = get_db()

    # Check if active drone with given id exists
    db_drone_info = db.execute('SELECT * FROM drones WHERE id = ?', (drone_id,)).fetchone()
    if db_drone_info is None:
        response = add_error_to_response(
            response,
            1,
            f'No active drone with id "{drone_id}" found.',
            False
        )

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    response['response_data'] = {
        'coordinates_lat': { 'age': 0, 'data': db_drone_info['coordinates_lat'] },
        'coordinates_lon': { 'age': 0, 'data': db_drone_info['coordinates_lon'] },
        'height':          { 'age': 0, 'data': db_drone_info['height'] },
        'heading':         { 'age': 0, 'data': db_drone_info['heading'] },
        'air_speed':       { 'age': 0, 'data': db_drone_info['air_speed'] },
        'ground_speed':    { 'age': 0, 'data': db_drone_info['ground_speed'] },
        'vertical_speed':  { 'age': 0, 'data': db_drone_info['vertical_speed'] },
        'flightplan': { 'age': 0, 'data': None },
        'health':  { 'age': 0, 'data': 'ok' },
        'battery_soc':     { 'age': 0, 'data': 85 },
        'rem_flight_time': { 'age': 0, 'data': 1500 }
    }

    return jsonify(response)
