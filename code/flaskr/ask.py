import functools

from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

import json

# Import own files
from functions_collection import *


bp = Blueprint('ask', __name__, url_prefix='/ask')


@bp.route('intersection_list')
def ask_intersection_list():
    response = get_response_template(response_data=True)

    # Get data formatted as JSON string
    payload_as_json_string = request.values.get('payload')

    response = check_argument_not_null(
        response, payload_as_json_string, 'payload')

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    # TODO: decrypt data

    payload = json.loads(payload_as_json_string)

    intersection_id = payload.get('intersection_id')
    data_type = payload.get('data_type')
    # data is not needed here

    response = check_argument_not_null(
        response, intersection_id, 'intersection_id')
    response = check_argument_not_null(response, data_type, 'data_type')

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    if not data_type == 'intersection_list':
        response = add_error_to_response(response,
                                         1,
                                         "'data_type' must be 'intersection_list'.",
                                         False)

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    db = get_db()

    # Get intersection information
    db_intersection_list = db.execute("""
        SELECT *
        FROM intersections
        WHERE id LIKE ?
        ESCAPE '!'
        """, (intersection_id,)).fetchall()

    response['response_data'] = {}
    for intersection in db_intersection_list:
        response['response_data'][intersection['id']] = {}
        response['response_data'][intersection['id']]['id'] = intersection['id']
        response['response_data'][intersection['id']]['gps_lat'] = intersection['gps_lat']
        response['response_data'][intersection['id']]['gps_lon'] = intersection['gps_lon']
        response['response_data'][intersection['id']]['altitude'] = intersection['altitude']

    return jsonify(response)


@bp.route('intersection_location')
def ask_intersection_location():
    response = get_response_template(response_data=True)

    # Get data formatted as JSON string
    payload_as_json_string = request.values.get('payload')

    response = check_argument_not_null(
        response, payload_as_json_string, 'payload')

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    # TODO: decrypt data

    payload = json.loads(payload_as_json_string)

    intersection_id = payload.get('intersection_id')
    data_type = payload.get('data_type')
    # data is not needed here

    response = check_argument_not_null(
        response, intersection_id, 'intersection_id')
    response = check_argument_not_null(response, data_type, 'data_type')

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    if not data_type == 'intersection_location':
        response = add_error_to_response(response,
                                         1,
                                         "'data_type' must be 'intersection_location'.",
                                         False)

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    db = get_db()

    # Get intersection information
    db_intersection_info = db.execute(
        'SELECT * FROM intersections WHERE id = ?', (intersection_id,)).fetchone()
    if db_intersection_info is None:
        response = add_error_to_response(
            response,
            1,
            f'Intersection with id "{intersection_id}" not found.',
            False
        )

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    response['response_data'] = {
        'gps_lat': db_intersection_info['gps_lat'],
        'gps_lon': db_intersection_info['gps_lon'],

        'altitude': db_intersection_info['altitude']
    }

    return jsonify(response)


@bp.route('corridor_list')
def ask_corridor_list():
    response = get_response_template(response_data=True)

    # Get data formatted as JSON string
    payload_as_json_string = request.values.get('payload')

    response = check_argument_not_null(
        response, payload_as_json_string, 'payload')

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    # TODO: decrypt data

    payload = json.loads(payload_as_json_string)

    corridor_id = payload.get('corridor_id')
    data_type = payload.get('data_type')
    # data is not needed here

    response = check_argument_not_null(
        response, corridor_id, 'corridor_id')
    response = check_argument_not_null(response, data_type, 'data_type')

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    if not data_type == 'corridor_list':
        response = add_error_to_response(response,
                                         1,
                                         "'data_type' must be 'corridor_list'.",
                                         False)

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    db = get_db()

    # Get intersection information
    db_corridor_list = db.execute("""
        SELECT *
        FROM corridors
        WHERE id LIKE ?
        ESCAPE '!'
        """, (corridor_id,)).fetchall()

    response['response_data'] = {}
    for corridor in db_corridor_list:
        response['response_data'][corridor['id']] = {}
        response['response_data'][corridor['id']]['id'] = corridor['id']
        response['response_data'][corridor['id']]['intersection_a'] = corridor['intersection_a']
        response['response_data'][corridor['id']]['intersection_b'] = corridor['intersection_b']

    return jsonify(response)


@bp.route('corridor_location')
def ask_corridor_location():
    response = get_response_template(response_data=True)

    # Get data formatted as JSON string
    payload_as_json_string = request.values.get('payload')

    response = check_argument_not_null(
        response, payload_as_json_string, 'payload')

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    # TODO: decrypt data

    payload = json.loads(payload_as_json_string)

    corridor_id = payload.get('corridor_id')
    data_type = payload.get('data_type')
    # data is not needed here

    response = check_argument_not_null(response, corridor_id, 'corridor_id')
    response = check_argument_not_null(response, data_type, 'data_type')

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    if not data_type == 'corridor_location':
        response = add_error_to_response(response,
                                         1,
                                         "'data_type' must be 'corridor_location'.",
                                         False)

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    db = get_db()

    # Get corridor information
    db_corridor_info = db.execute(
        'SELECT * FROM corridors WHERE id = ?', (corridor_id,)).fetchone()
    if db_corridor_info is None:
        response = add_error_to_response(
            response,
            1,
            f'Corridor with id "{corridor_id}" not found.',
            False
        )

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    response['response_data'] = {
        'intersection_a': db_corridor_info['intersection_a'],
        'intersection_b': db_corridor_info['intersection_b']
    }

    return jsonify(response)


@bp.route('drone_ids')
def ask_drone_ids():
    response = get_response_template(response_data=True)

    # Get data formatted as JSON string
    payload_as_json_string = request.values.get('payload')

    response = check_argument_not_null(
        response, payload_as_json_string, 'payload')

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    # TODO: decrypt data

    payload = json.loads(payload_as_json_string)

    drone_id = payload.get('drone_id')
    data_type = payload.get('data_type')
    # data is not needed here

    response = check_argument_not_null(response, drone_id, 'drone_id')
    response = check_argument_not_null(response, data_type, 'data_type')

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    if not data_type == 'drone_ids':
        response = add_error_to_response(response,
                                         1,
                                         "'data_type' must be 'drone_ids'.",
                                         False)

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    db = get_db()

    # Get drone ids
    db_drone_info = db.execute("""
        SELECT id
        FROM drones
        WHERE id LIKE ?
        ESCAPE '!'
        """, (drone_id,)).fetchall()

    response['response_data'] = { 'drone_ids': [] }
    for drone in db_drone_info:
        response['response_data']['drone_ids'].append(drone['id'])

    return jsonify(response)


@bp.route('aircraft_location_ids')
def ask_aircraft_location_ids():
    response = get_response_template(response_data=True)

    # Get data formatted as JSON string
    payload_as_json_string = request.values.get('payload')

    response = check_argument_not_null(
        response, payload_as_json_string, 'payload')

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    # TODO: decrypt data

    payload = json.loads(payload_as_json_string)

    drone_id = payload.get('drone_id')
    data_type = payload.get('data_type')
    # data is not needed here

    response = check_argument_not_null(response, drone_id, 'drone_id')
    response = check_argument_not_null(response, data_type, 'data_type')

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    if not data_type == 'aircraft_location_ids':
        response = add_error_to_response(response,
                                         1,
                                         "'data_type' must be 'aircraft_location_ids'.",
                                         False)

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    db = get_db()

    # Get aircraft_location ids
    db_aircraft_location_info = db.execute("""
        SELECT min(id) as min_id, max(id) as max_id
        FROM aircraft_location
        WHERE drone_id = ?
        """, (drone_id,)).fetchone()

    response['response_data'] = {
        'min_id': db_aircraft_location_info['min_id'],
        'max_id': db_aircraft_location_info['max_id']
        }

    return jsonify(response)


@bp.route('aircraft_location')
def ask_aircraft_location():
    response = get_response_template(response_data=True)

    # Get data formatted as JSON string
    payload_as_json_string = request.values.get('payload')

    response = check_argument_not_null(
        response, payload_as_json_string, 'payload')

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    # TODO: decrypt data

    payload = json.loads(payload_as_json_string)

    drone_id = payload.get('drone_id')
    data_type = payload.get('data_type')
    data = payload.get('data')  # can be None

    response = check_argument_not_null(response, drone_id, 'drone_id')
    response = check_argument_not_null(response, data_type, 'data_type')

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    if not data_type == 'aircraft_location':
        response = add_error_to_response(response,
                                         1,
                                         "'data_type' must be 'aircraft_location'.",
                                         False)

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    db = get_db()

    # Check if drone with given id exists
    db_drone_id = db.execute(
        'SELECT id FROM drones WHERE id = ?', (drone_id,)).fetchone()
    if db_drone_id is None:
        response = add_error_to_response(
            response,
            1,
            f'Drone with id "{drone_id}" not found.',
            False
        )

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    # Get aircraft_location data
    db_drone_info = None
    if data is None:
        # Get latest entry
        db_drone_info = db.execute("""
            SELECT * FROM aircraft_location
            WHERE drone_id = ?
            ORDER BY id DESC
            """, (drone_id,)).fetchone()
    else:
        # Get specific entry
        data_id = data.get('data_id')

        response = check_argument_not_null(response, data_id, 'data_id')

        # Return if an error already occured
        if not response['executed']:
            return jsonify(response)

        response, data_id = check_argument_type(
            response, data_id, 'data_id', 'int')

        # Return if an error already occured
        if not response['executed']:
            return jsonify(response)

        db_drone_info = db.execute("""
            SELECT * FROM aircraft_location
            WHERE drone_id = ?
                  AND id = ?
            """, (drone_id, data_id,)).fetchone()

    if not db_drone_info is None:
        response['response_data'] = {
            'transaction_uuid': db_drone_info['transaction_uuid'],

            'gps_signal_level': db_drone_info['gps_signal_level'],
            'gps_satellites_connected': db_drone_info['gps_satellites_connected'],

            'gps_valid':  strtobool(db_drone_info['gps_valid']),
            'gps_lat':    db_drone_info['gps_lat'],
            'gps_lon':    db_drone_info['gps_lon'],

            'altitude':   db_drone_info['altitude'],

            'velocity_x': db_drone_info['velocity_x'],
            'velocity_y': db_drone_info['velocity_y'],
            'velocity_z': db_drone_info['velocity_z'],

            'pitch':      db_drone_info['pitch'],
            'yaw':        db_drone_info['yaw'],
            'roll':       db_drone_info['roll']
        }

    return jsonify(response)


@bp.route('aircraft_power_ids')
def ask_aircraft_power_ids():
    response = get_response_template(response_data=True)

    # Get data formatted as JSON string
    payload_as_json_string = request.values.get('payload')

    response = check_argument_not_null(
        response, payload_as_json_string, 'payload')

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    # TODO: decrypt data

    payload = json.loads(payload_as_json_string)

    drone_id = payload.get('drone_id')
    data_type = payload.get('data_type')
    # data is not needed here

    response = check_argument_not_null(response, drone_id, 'drone_id')
    response = check_argument_not_null(response, data_type, 'data_type')

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    if not data_type == 'aircraft_power_ids':
        response = add_error_to_response(response,
                                         1,
                                         "'data_type' must be 'aircraft_power_ids'.",
                                         False)

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    db = get_db()

    # Get aircraft_power ids
    db_aircraft_power_info = db.execute("""
        SELECT min(id) as min_id, max(id) as max_id
        FROM aircraft_power
        WHERE drone_id = ?
        """, (drone_id,)).fetchone()

    response['response_data'] = {
        'min_id': db_aircraft_power_info['min_id'],
        'max_id': db_aircraft_power_info['max_id']
        }

    return jsonify(response)


@bp.route('aircraft_power')
def ask_aircraft_power():
    response = get_response_template(response_data=True)

    # Get data formatted as JSON string
    payload_as_json_string = request.values.get('payload')

    response = check_argument_not_null(
        response, payload_as_json_string, 'payload')

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    # TODO: decrypt data

    payload = json.loads(payload_as_json_string)

    drone_id = payload.get('drone_id')
    data_type = payload.get('data_type')
    data = payload.get('data')  # can be None

    response = check_argument_not_null(response, drone_id, 'drone_id')
    response = check_argument_not_null(response, data_type, 'data_type')

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    if not data_type == 'aircraft_power':
        response = add_error_to_response(response,
                                         1,
                                         "'data_type' must be 'aircraft_power'.",
                                         False)

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    db = get_db()

    # Check if drone with given id exists
    db_drone_id = db.execute(
        'SELECT id FROM drones WHERE id = ?', (drone_id,)).fetchone()
    if db_drone_id is None:
        response = add_error_to_response(
            response,
            1,
            f'Drone with id "{drone_id}" not found.',
            False
        )

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    # Get aircraft_power data
    db_aircraft_power_info = None
    if data is None:
        # Get latest entry
        db_aircraft_power_info = db.execute("""
            SELECT * FROM aircraft_power
            WHERE drone_id = ?
            ORDER BY id DESC
            """, (drone_id,)).fetchone()
    else:
        # Get specific entry
        data_id = data.get('data_id')

        response = check_argument_not_null(response, data_id, 'data_id')

        # Return if an error already occured
        if not response['executed']:
            return jsonify(response)

        response, data_id = check_argument_type(
            response, data_id, 'data_id', 'int')

        # Return if an error already occured
        if not response['executed']:
            return jsonify(response)

        db_aircraft_power_info = db.execute("""
            SELECT * FROM aircraft_power
            WHERE drone_id = ?
                  AND id = ?
            """, (drone_id, data_id,)).fetchone()

    if not db_aircraft_power_info is None:
        response['response_data'] = {
            'transaction_uuid': db_aircraft_power_info['transaction_uuid'],

            'battery_remaining': db_aircraft_power_info['battery_remaining'],
            'battery_remaining_percent': db_aircraft_power_info['battery_remaining_percent'],

            'remaining_flight_time': db_aircraft_power_info['remaining_flight_time'],
            'remaining_flight_radius': db_aircraft_power_info['remaining_flight_radius']
        }

    return jsonify(response)


@bp.route('flight_data_ids')
def ask_flight_data_ids():
    response = get_response_template(response_data=True)

    # Get data formatted as JSON string
    payload_as_json_string = request.values.get('payload')

    response = check_argument_not_null(
        response, payload_as_json_string, 'payload')

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    # TODO: decrypt data

    payload = json.loads(payload_as_json_string)

    drone_id = payload.get('drone_id')
    data_type = payload.get('data_type')
    # data is not needed here

    response = check_argument_not_null(response, drone_id, 'drone_id')
    response = check_argument_not_null(response, data_type, 'data_type')

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    if not data_type == 'flight_data_ids':
        response = add_error_to_response(response,
                                         1,
                                         "'data_type' must be 'flight_data_ids'.",
                                         False)

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    db = get_db()

    # Get flight_data ids
    db_flight_data_info = db.execute("""
        SELECT min(id) as min_id, max(id) as max_id
        FROM flight_data
        WHERE drone_id = ?
        """, (drone_id,)).fetchone()

    response['response_data'] = {
        'min_id': db_flight_data_info['min_id'],
        'max_id': db_flight_data_info['max_id']
        }

    return jsonify(response)


@bp.route('flight_data')
def ask_flight_data():
    response = get_response_template(response_data=True)

    # Get data formatted as JSON string
    payload_as_json_string = request.values.get('payload')

    response = check_argument_not_null(
        response, payload_as_json_string, 'payload')

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    # TODO: decrypt data

    payload = json.loads(payload_as_json_string)

    drone_id = payload.get('drone_id')
    data_type = payload.get('data_type')
    data = payload.get('data')  # can be None

    response = check_argument_not_null(response, drone_id, 'drone_id')
    response = check_argument_not_null(response, data_type, 'data_type')

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    if not data_type == 'flight_data':
        response = add_error_to_response(response,
                                         1,
                                         "'data_type' must be 'flight_data'.",
                                         False)

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    db = get_db()

    # Check if drone with given id exists
    db_drone_id = db.execute(
        'SELECT id FROM drones WHERE id = ?', (drone_id,)).fetchone()
    if db_drone_id is None:
        response = add_error_to_response(
            response,
            1,
            f'Drone with id "{drone_id}" not found.',
            False
        )

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    # Get aircraft_power data
    db_flight_data_info = None
    if data is None:
        # Get latest entry
        db_flight_data_info = db.execute("""
            SELECT * FROM flight_data
            WHERE drone_id = ?
            ORDER BY id DESC
            """, (drone_id,)).fetchone()
    else:
        # Get specific entry
        data_id = data.get('data_id')

        response = check_argument_not_null(response, data_id, 'data_id')

        # Return if an error already occured
        if not response['executed']:
            return jsonify(response)

        response, data_id = check_argument_type(
            response, data_id, 'data_id', 'int')

        # Return if an error already occured
        if not response['executed']:
            return jsonify(response)

        db_flight_data_info = db.execute("""
            SELECT * FROM flight_data
            WHERE drone_id = ?
                  AND id = ?
            """, (drone_id, data_id,)).fetchone()

    if not db_flight_data_info is None:
        response['response_data'] = {
            'transaction_uuid': db_flight_data_info['transaction_uuid'],

            'takeoff_time': db_flight_data_info['takeoff_time'],
            'takeoff_gps_valid': db_flight_data_info['takeoff_gps_valid'],
            'takeoff_gps_lat': db_flight_data_info['takeoff_gps_lat'],
            'takeoff_gps_lon': db_flight_data_info['takeoff_gps_lon'],

            'landing_time': db_flight_data_info['landing_time'],
            'landing_gps_valid': db_flight_data_info['landing_gps_valid'],
            'landing_gps_lat': db_flight_data_info['landing_gps_lat'],
            'landing_gps_lon': db_flight_data_info['landing_gps_lon'],

            'operation_modes': json.loads(db_flight_data_info['operation_modes'])
        }

    return jsonify(response)
