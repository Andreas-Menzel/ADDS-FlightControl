import functools

from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

# Import own files
from functions_collection import *


bp = Blueprint('tell', __name__, url_prefix='/tell')


@bp.route('/here_i_am')
def here_i_am():
    response = get_response_template()

    drone_id        = request.values.get('drone_id')
    coordinates_lat = request.values.get('coordinates_lat')
    coordinates_lon = request.values.get('coordinates_lon')
    height          = request.values.get('height')
    heading         = request.values.get('heading')
    air_speed       = request.values.get('air_speed')
    ground_speed    = request.values.get('ground_speed')
    vertical_speed  = request.values.get('vertical_speed')

    # Check if all required values were given
    response = check_argument_not_null(response, drone_id, 'drone_id')
    response = check_argument_not_null(response, coordinates_lat, 'coordinates_lat')
    response = check_argument_not_null(response, coordinates_lon, 'coordinates_lon')
    response = check_argument_not_null(response, height, 'height')
    response = check_argument_not_null(response, heading, 'heading')
    
    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    db = get_db()

    # Check if drone with given id exists
    tmp_db_drone_id = db.execute('SELECT id FROM drones WHERE id = ?', (drone_id,)).fetchone()
    if tmp_db_drone_id is None:
        response = add_error_to_response(
            response,
            1,
            f'No drone with id "{drone_id}" found',
            False
        )
    
    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    try:
        db.execute("""
        UPDATE drones
        SET coordinates_lat = ?,
            coordinates_lon = ?,
            height = ?,
            heading = ?
        WHERE id = ?
        """, (coordinates_lat, coordinates_lon, height, heading, drone_id,))

        # TODO: air_speed, ground_speed, vertical_speed (calculate & set)

        db.commit()
    except db.IntegrityError:
        response = add_error_to_response(
            response,
            1,
            'Internal server error: IntegrityError while accessing the database',
            False
        )

    return jsonify(response)


@bp.route('/my_health')
def my_health():
    response = get_response_template()

    drone_id        = request.values.get('drone_id')
    health          = request.values.get('health')
    battery_soc     = request.values.get('battery_soc')
    rem_flight_time = request.values.get('rem_flight_time')
    
    # Check if all required values were given
    response = check_argument_not_null(response, drone_id, 'drone_id')
    response = check_argument_not_null(response, health, 'health')
    response = check_argument_not_null(response, battery_soc, 'battery_soc')
    
    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)
    
    # Check if drone with given id exists
    tmp_db_drone_id = db.execute('SELECT id FROM drones WHERE id = ?', (drone_id,)).fetchone()
    if tmp_db_drone_id is None:
        response = add_error_to_response(
            response,
            1,
            f'Drone with id "{drone_id}" does not exist.',
            False
        )
    
    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    try:
        db.execute("""
        UPDATE drones
        SET health = ?,
            battery_soc = ?,
            rem_flight_time = ?
        WHERE id = ?
        """, (health, battery_soc, rem_flight_time, drone_id,))

        db.commit()
    except db.IntegrityError:
        response = add_error_to_response(
            response,
            1,
            'Internal server error: IntegrityError while accessing the database',
            False
        )

    return jsonify(response)


@bp.route('register_drone')
def register_drone():
    response = get_response_template()

    drone_id = request.values.get('drone_id')
    
    # Check if all required values were given
    response = check_argument_not_null(response, drone_id, 'drone_id')
    
    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    db = get_db()

    # Check if drone with this id already exists
    db_drone = db.execute('SELECT id FROM drones WHERE id = ?', (drone_id,)).fetchone()
    if db_drone is None:
        db.execute('INSERT INTO drones(id) VALUES(?)', (drone_id,))
        
        db.commit()
    else:
        response = add_warning_to_response(
            response,
            1,
            f'Drone with id "{drone_id}" already exists.'
        )

    return jsonify(response)


@bp.route('deregister_drone')
def deregister_drone():
    response = get_response_template()

    drone_id = request.values.get('drone_id')
    
    # Check if all required values were given
    response = check_argument_not_null(response, drone_id, 'drone_id')
    
    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    db = get_db()

    db_drone = db.execute('SELECT id, active FROM drones WHERE id = ?', (drone_id,)).fetchone()
    
    # Check if drone with this id exists
    if not db_drone is None:
        if not db_drone['active']:
            db.execute('DELETE FROM drones WHERE id = ?', (drone_id,))
            
            db.commit()
        else:
            response = add_error_to_response(
                response,
                1,
                f'Drone with id "{drone_id}" is still active.',
                False
            )
    else:
        response = add_warning_to_response(
            response,
            1,
            f'Drone with id "{drone_id}" does not exist.'
        )

    return jsonify(response)


@bp.route('/activate_drone')
def activate_drone():
    response = get_response_template()

    drone_id = request.values.get('drone_id')
    
    # Check if all required values were given
    response = check_argument_not_null(response, drone_id, 'drone_id')
    
    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    db = get_db()

    db_drone = db.execute('SELECT id, active FROM drones WHERE id = ?', (drone_id,)).fetchone()

    # Check if drone with given id exists
    if db_drone is None:
        response = add_error_to_response(
            response,
            1,
            f'Drone with id "{drone_id}" does not exist.',
            False
        )
    
    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    if not db_drone['active']:
        try:
            db.execute('UPDATE drones SET active = TRUE WHERE id = ?', (drone_id,))
            db.commit()
        except db.IntegrityError:
            response = add_error_to_response(
                response,
                1,
                'Internal server error: IntegrityError while accessing the database',
                False
            )
    else:
        response = add_warning_to_response(
            response,
            1,
            f'Drone with id "{drone_id}" already active.'
        )

    return jsonify(response)


@bp.route('/deactivate_drone')
def deactivate_drone():
    response = get_response_template()

    drone_id = request.values.get('drone_id')
    
    # Check if all required values were given
    response = check_argument_not_null(response, drone_id, 'drone_id')
    
    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    db = get_db()

    db_drone = db.execute('SELECT id, active FROM drones WHERE id = ?', (drone_id,)).fetchone()

    # Check if drone with given id exists
    if db_drone is None:
        response = add_error_to_response(
            response,
            1,
            f'Drone with id "{drone_id}" does not exist.',
            False
        )
    
    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    if db_drone['active']:
        try:
            db.execute('UPDATE drones SET active = FALSE WHERE id = ?', (drone_id,))
            db.commit()
        except db.IntegrityError:
            response = add_error_to_response(
                response,
                1,
                'Internal server error: IntegrityError while accessing the database',
                False
            )
    else:
        response = add_warning_to_response(
            response,
            1,
            f'Drone with id "{drone_id}" not active.'
        )

    return jsonify(response)
