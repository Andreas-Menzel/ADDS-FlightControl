import functools

from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

import json

# Import own files
from functions_collection import *


bp = Blueprint('tell', __name__, url_prefix='/tell')



@bp.route('aircraft_location')
def tell_aircraft_location():
    response = get_response_template()

    # Get data formatted as JSON string
    payload_as_json_string = request.values.get('payload')

    response = check_argument_not_null(response, payload_as_json_string, 'payload')

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    # TODO: decrypt data

    payload = json.loads(payload_as_json_string)

    drone_id = payload['drone_id']
    data_type = payload['data_type']
    data = payload['data']

    response = check_argument_not_null(response, drone_id, 'drone_id')
    response = check_argument_not_null(response, data_type, 'data_type')
    response = check_argument_not_null(response, data, 'data')

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    if not data_type == 'aircraft_location':
        response = add_error_to_response(response,
                                         1,
                                         "'data_type' must be 'aircraft_location'.")

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    gps_signal_level = data['gps_signal_level']
    gps_satellites_connected = data['gps_satellites_connected']
    gps_valid = data['gps_valid']
    gps_lat = data['gps_lat']
    gps_lon = data['gps_lon']
    altitude = data['altitude']
    velocity_x = data['velocity_x']
    velocity_y = data['velocity_y']
    velocity_z = data['velocity_z']
    pitch = data['pitch']
    yaw = data['yaw']
    roll = data['roll']

    response = check_argument_not_null(
        response, gps_signal_level, 'gps_signal_level')
    response = check_argument_not_null(
        response, gps_satellites_connected, 'gps_satellites_connected')
    response = check_argument_not_null(response, gps_valid, 'gps_valid')
    response = check_argument_not_null(response, gps_lat, 'gps_lat')
    response = check_argument_not_null(response, gps_lon, 'gps_lon')
    response = check_argument_not_null(response, altitude, 'altitude')
    response = check_argument_not_null(response, velocity_x, 'velocity_x')
    response = check_argument_not_null(response, velocity_y, 'velocity_y')
    response = check_argument_not_null(response, velocity_z, 'velocity_z')
    response = check_argument_not_null(response, pitch, 'pitch')
    response = check_argument_not_null(response, yaw, 'yaw')
    response = check_argument_not_null(response, roll, 'roll')

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    # Convert variables to correct type
    response, gps_signal_level = check_argument_type(
        response, gps_signal_level, 'gps_signal_level', 'int')
    response, gps_satellites_connected = check_argument_type(
        response, gps_satellites_connected, 'gps_satellites_connected', 'int')
    response, gps_valid = check_argument_type(
        response, gps_valid, 'gps_valid', 'boolean')
    response, gps_lat = check_argument_type(
        response, gps_lat, 'gps_lat', 'float')
    response, gps_lon = check_argument_type(
        response, gps_lon, 'gps_lon', 'float')
    response, altitude = check_argument_type(
        response, altitude, 'altitude', 'float')
    response, velocity_x = check_argument_type(
        response, velocity_x, 'velocity_x', 'float')
    response, velocity_y = check_argument_type(
        response, velocity_y, 'velocity_y', 'float')
    response, velocity_z = check_argument_type(
        response, velocity_z, 'velocity_z', 'float')
    response, pitch = check_argument_type(
        response, pitch, 'pitch', 'float')
    response, yaw = check_argument_type(response, yaw, 'yaw', 'float')
    response, roll = check_argument_type(response, roll, 'roll', 'float')

    # TODO: Check if value sets are complete (gps_lat & gps_lon, pitch & yaw & roll)

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    db = get_db()

    # Check if drone with given id exists
    tmp_db_drone_id = db.execute(
        'SELECT id FROM drones WHERE id = ?', (drone_id,)).fetchone()
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
            SET gps_signal_level = ?,
                gps_satellites_connected = ?,
                gps_valid = ?,
                gps_lat = ?,
                gps_lon = ?,
                altitude = ?,
                velocity_x = ?,
                velocity_y = ?,
                velocity_z = ?,
                pitch = ?,
                yaw = ?,
                roll = ?,
            WHERE id = ?
            """, (gps_signal_level, gps_satellites_connected, gps_valid, gps_lat, gps_lon, altitude, velocity_x, velocity_y, velocity_z, pitch, yaw, roll, drone_id,)
        )

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

    drone_id = request.values.get('drone_id')
    health = request.values.get('health')
    battery_remaining = request.values.get('battery_remaining')
    battery_remaining_percent = request.values.get('battery_remaining_percent')
    remaining_flight_time = request.values.get('remaining_flight_time')
    remaining_flight_radius = request.values.get('remaining_flight_radius')

    # Check if all required values were given
    response = check_argument_not_null(response, drone_id, 'drone_id')
    response = check_argument_not_null(response, health, 'health')
    response = check_argument_not_null(
        response, battery_remaining_percent, 'battery_remaining_percent')

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    # Convert variables to correct type
    if not battery_remaining is None:
        response, battery_remaining = check_argument_type(
            response, battery_remaining, 'battery_remaining', 'int')
    if not battery_remaining_percent is None:
        response, battery_remaining_percent = check_argument_type(
            response, battery_remaining_percent, 'battery_remaining_percent', 'int')
    if not remaining_flight_time is None:
        response, remaining_flight_time = check_argument_type(
            response, remaining_flight_time, 'remaining_flight_time', 'int')
    if not remaining_flight_radius is None:
        response, remaining_flight_radius = check_argument_type(
            response, remaining_flight_radius, 'remaining_flight_radius', 'float')

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    db = get_db()

    # Check if drone with given id exists
    tmp_db_drone_id = db.execute(
        'SELECT id FROM drones WHERE id = ?', (drone_id,)).fetchone()
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
            SET health = ?,
                battery_remaining_percent = ?
            WHERE id = ?
            """, (health, battery_remaining_percent, drone_id,)
        )

        # Update battery_remaining if is set
        if not battery_remaining is None:
            db.execute("""
            UPDATE drones
            SET battery_remaining = ?
            WHERE id = ?
            """, (battery_remaining, drone_id,)
            )

        # Update remaining_flight_time if is set
        if not remaining_flight_time is None:
            db.execute("""
            UPDATE drones
            SET remaining_flight_time = ?
            WHERE id = ?
            """, (remaining_flight_time, drone_id,)
            )

        # Update remaining_flight_radius if is set
        if not remaining_flight_radius is None:
            db.execute("""
            UPDATE drones
            SET remaining_flight_radius = ?
            WHERE id = ?
            """, (remaining_flight_radius, drone_id,)
            )

        db.commit()
    except db.IntegrityError:
        response = add_error_to_response(
            response,
            1,
            'Internal server error: IntegrityError while accessing the database.',
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
    db_drone = db.execute(
        'SELECT id FROM drones WHERE id = ?', (drone_id,)).fetchone()
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

    db_drone = db.execute(
        'SELECT id, active FROM drones WHERE id = ?', (drone_id,)).fetchone()

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

    db_drone = db.execute(
        'SELECT id, active FROM drones WHERE id = ?', (drone_id,)).fetchone()

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
            db.execute(
                'UPDATE drones SET active = TRUE WHERE id = ?', (drone_id,))
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

    db_drone = db.execute(
        'SELECT id, active FROM drones WHERE id = ?', (drone_id,)).fetchone()

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
            db.execute(
                'UPDATE drones SET active = FALSE WHERE id = ?', (drone_id,))
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
