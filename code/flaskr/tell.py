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

    # Get values from URL (or POST)
    drone_id  = request.values.get('drone_id')
    gps_signal_level = request.values.get('gps_signal_level')
    gps_satellites_connected = request.values.get('gps_satellites_connected')
    gps_valid = request.values.get('gps_valid')
    gps_lat   = request.values.get('gps_lat')
    gps_lon   = request.values.get('gps_lon')
    altitude  = request.values.get('altitude')
    pitch     = request.values.get('pitch')
    yaw       = request.values.get('yaw')
    roll      = request.values.get('roll')

    # Check if all required values were given
    response = check_argument_not_null(response, drone_id, 'drone_id')
    response = check_argument_not_null(response, gps_valid, 'gps_valid')
    response = check_argument_not_null(response, gps_lat, 'gps_lat')
    response = check_argument_not_null(response, gps_lon, 'gps_lon')
    response = check_argument_not_null(response, altitude, 'altitude')
    
    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)
    
    # Convert variables to correct type
    if not gps_signal_level == None:
        response, gps_signal_level = check_argument_type(response, gps_signal_level, 'gps_signal_level', 'int')
    if not gps_satellites_connected == None:
        response, gps_satellites_connected = check_argument_type(response, gps_satellites_connected, 'gps_satellites_connected', 'int')
    if not gps_valid == None:
        response, gps_valid = check_argument_type(response, gps_valid, 'gps_valid', 'boolean')
    if not gps_lat == None:
        response, gps_lat = check_argument_type(response, gps_lat, 'gps_lat', 'float')
    if not gps_lon == None:
        response, gps_lat = check_argument_type(response, gps_lon, 'gps_lon', 'float')
    if not altitude == None:
        response, altitude = check_argument_type(response, altitude, 'altitude', 'float')
    if not pitch == None:
        response, pitch = check_argument_type(response, pitch, 'pitch', 'float')
    if not yaw == None:
        response, yaw = check_argument_type(response, yaw, 'yaw', 'float')
    if not roll == None:
        response, roll = check_argument_type(response, roll, 'roll', 'float')

    # TODO: Check if value sets are complete (gps_lat & gps_lon, pitch & yaw & roll)

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
            f'Drone with id "{drone_id}" not found.',
            False
        )
    
    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    try:
        # Update all required fields
        db.execute("""
            UPDATE drones
            SET gps_valid = ?,
                gps_lat = ?,
                gps_lon = ?,
                altitude = ?
            WHERE id = ?
            """, (gps_valid, gps_lat, gps_lon, altitude, drone_id,)
        )

        # Update gps_signal_level if is set
        if not gps_signal_level == None:
            db.execute("""
            UPDATE drones
            SET gps_signal_level = ?
            WHERE id = ?
            """, (gps_signal_level, drone_id,))
        
        # Update gps_satellites_connected if is set
        if not gps_satellites_connected == None:
            db.execute("""
            UPDATE drones
            SET gps_satellites_connected = ?
            WHERE id = ?
            """, (gps_satellites_connected, drone_id,))
        
        # Update pitch if is set
        if not pitch == None:
            db.execute("""
            UPDATE drones
            SET pitch = ?
            WHERE id = ?
            """, (pitch, drone_id,))
        
        # Update yaw if is set
        if not yaw == None:
            db.execute("""
            UPDATE drones
            SET yaw = ?
            WHERE id = ?
            """, (yaw, drone_id,))
        
        # Update roll if is set
        if not roll == None:
            db.execute("""
            UPDATE drones
            SET roll = ?
            WHERE id = ?
            """, (roll, drone_id,))

        db.commit()
    except db.IntegrityError:
        response = add_error_to_response(
            response,
            1,
            'Internal server error: IntegrityError while accessing the database.',
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
