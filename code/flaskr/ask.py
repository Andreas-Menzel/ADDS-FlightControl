import functools

from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

import json
import math
import networkx as nx

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
        FROM (
            SELECT *
            FROM intersections
            LEFT JOIN locked_intersections
              ON intersections.id = locked_intersections.intersection_id
        )
        WHERE id LIKE ?
        ESCAPE '!'
        """, (intersection_id,)).fetchall()

    response['response_data'] = {}
    for intersection in db_intersection_list:
        response['response_data'][intersection['id']] = {}
        response['response_data'][intersection['id']
                                  ]['id'] = intersection['id']
        response['response_data'][intersection['id']
                                  ]['gps_lat'] = intersection['gps_lat']
        response['response_data'][intersection['id']
                                  ]['gps_lon'] = intersection['gps_lon']
        response['response_data'][intersection['id']
                                  ]['altitude'] = intersection['altitude']
        response['response_data'][intersection['id']
                                  ]['locked_by'] = intersection['drone_id']

    response = check_and_update_infrastructure_locks(response, db)

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
        FROM (
            SELECT *
            FROM corridors
            LEFT JOIN locked_corridors
              ON corridors.id = locked_corridors.corridor_id
        )
        WHERE id LIKE ?
        ESCAPE '!'
        """, (corridor_id,)).fetchall()

    response['response_data'] = {}
    for corridor in db_corridor_list:
        response['response_data'][corridor['id']] = {}
        response['response_data'][corridor['id']]['id'] = corridor['id']
        response['response_data'][corridor['id']
                                  ]['intersection_a'] = corridor['intersection_a']
        response['response_data'][corridor['id']
                                  ]['intersection_b'] = corridor['intersection_b']
        response['response_data'][corridor['id']
                                  ]['locked_by'] = corridor['drone_id']

    response = check_and_update_infrastructure_locks(response, db)

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

    response['response_data'] = {'drone_ids': []}
    for drone in db_drone_info:
        response['response_data']['drone_ids'].append(drone['id'])

    return jsonify(response)


@bp.route('drone_list')
def ask_drone_list():
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

    if not data_type == 'drone_list':
        response = add_error_to_response(response,
                                         1,
                                         "'data_type' must be 'drone_list'.",
                                         False)

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    db = get_db()

    # Get drones
    db_drone_info = db.execute("""
        SELECT
            d.id,
            d.chain_uuid_mission,
            d.chain_uuid_blackbox,
            IFNULL(al.latest_time_sent, 0) latest_time_sent_aircraft_location,
            IFNULL(ap.latest_time_sent, 0) latest_time_sent_aircraft_power,
            IFNULL(fd.latest_time_sent, 0) latest_time_sent_flight_data,
            IFNULL(al.latest_time_recorded, 0) latest_time_recorded_aircraft_location,
            IFNULL(ap.latest_time_recorded, 0) latest_time_recorded_aircraft_power,
            IFNULL(fd.latest_time_recorded, 0) latest_time_recorded_flight_data
        FROM drones d
        LEFT JOIN (
            SELECT drone_id, MAX(time_sent) latest_time_sent, MAX(time_recorded) latest_time_recorded
            FROM aircraft_location
            GROUP BY drone_id
        ) al ON d.id = al.drone_id
        LEFT JOIN (
            SELECT drone_id, MAX(time_sent) latest_time_sent, MAX(time_recorded) latest_time_recorded
            FROM aircraft_power
            GROUP BY drone_id
        ) ap ON d.id = ap.drone_id
        LEFT JOIN (
            SELECT drone_id, MAX(time_sent) latest_time_sent, MAX(time_recorded) latest_time_recorded
            FROM flight_data
            GROUP BY drone_id
        ) fd ON d.id = fd.drone_id
        WHERE id LIKE ?
        ESCAPE '!'
        ;
        """, (drone_id,)).fetchall()

    response['response_data'] = {}
    for drone in db_drone_info:
        response['response_data'][drone['id']] = {}
        response['response_data'][drone['id']]['id'] = drone['id']
        response['response_data'][drone['id']
                                  ]['chain_uuid_mission'] = drone['chain_uuid_mission']
        response['response_data'][drone['id']
                                  ]['chain_uuid_blackbox'] = drone['chain_uuid_blackbox']
        response['response_data'][drone['id']
                                  ]['latest_time_sent_aircraft_location'] = drone['latest_time_sent_aircraft_location']
        response['response_data'][drone['id']
                                  ]['latest_time_sent_aircraft_power'] = drone['latest_time_sent_aircraft_power']
        response['response_data'][drone['id']
                                  ]['latest_time_sent_flight_data'] = drone['latest_time_sent_flight_data']
        response['response_data'][drone['id']
                                  ]['latest_time_recorded_aircraft_location'] = drone['latest_time_recorded_aircraft_location']
        response['response_data'][drone['id']
                                  ]['latest_time_recorded_aircraft_power'] = drone['latest_time_recorded_aircraft_power']
        response['response_data'][drone['id']
                                  ]['latest_time_recorded_flight_data'] = drone['latest_time_recorded_flight_data']

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
            'time_sent': db_drone_info['time_sent'],
            'time_recorded': db_drone_info['time_recorded'],

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
            'time_sent': db_aircraft_power_info['time_sent'],
            'time_recorded': db_aircraft_power_info['time_recorded'],

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

    # Get flight_data data
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
        operation_modes_string = db_flight_data_info['operation_modes']
        operation_modes = None
        if not operation_modes_string is None:
            operation_modes = json.loads(operation_modes_string)

        response['response_data'] = {
            'time_sent': db_flight_data_info['time_sent'],
            'time_recorded': db_flight_data_info['time_recorded'],

            'transaction_uuid': db_flight_data_info['transaction_uuid'],

            'takeoff_time': db_flight_data_info['takeoff_time'],
            'takeoff_gps_valid': strtobool(db_flight_data_info['takeoff_gps_valid']),
            'takeoff_gps_lat': db_flight_data_info['takeoff_gps_lat'],
            'takeoff_gps_lon': db_flight_data_info['takeoff_gps_lon'],

            'landing_time': db_flight_data_info['landing_time'],
            'landing_gps_valid': strtobool(db_flight_data_info['landing_gps_valid']),
            'landing_gps_lat': db_flight_data_info['landing_gps_lat'],
            'landing_gps_lon': db_flight_data_info['landing_gps_lon'],

            'operation_modes': operation_modes
        }

    return jsonify(response)


@bp.route('mission_data_ids')
def ask_mission_data_ids():
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

    if not data_type == 'mission_data_ids':
        response = add_error_to_response(response,
                                         1,
                                         "'data_type' must be 'mission_data_ids'.",
                                         False)

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    db = get_db()

    # Get flight_data ids
    db_mission_data_info = db.execute("""
        SELECT min(id) as min_id, max(id) as max_id
        FROM mission_data
        WHERE drone_id = ?
        """, (drone_id,)).fetchone()

    response['response_data'] = {
        'min_id': db_mission_data_info['min_id'],
        'max_id': db_mission_data_info['max_id']
    }

    return jsonify(response)


@bp.route('mission_data')
def ask_mission_data():
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

    if not data_type == 'mission_data':
        response = add_error_to_response(response,
                                         1,
                                         "'data_type' must be 'mission_data'.",
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

    # Get mission_data data
    db_mission_data_info = None
    if data is None:
        # Get latest entry
        db_mission_data_info = db.execute("""
            SELECT * FROM mission_data
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

        db_mission_data_info = db.execute("""
            SELECT * FROM mission_data
            WHERE drone_id = ?
                  AND id = ?
            """, (drone_id, data_id,)).fetchone()

    if not db_mission_data_info is None:
        corridors_pending_string = db_mission_data_info['corridors_pending']
        corridors_pending = None
        if not corridors_pending_string is None:
            corridors_pending = json.loads(corridors_pending_string)

        corridors_approved_string = db_mission_data_info['corridors_approved']
        corridors_approved = None
        if not corridors_approved_string is None:
            corridors_approved = json.loads(corridors_approved_string)

        corridors_uploaded_string = db_mission_data_info['corridors_uploaded']
        corridors_uploaded = None
        if not corridors_uploaded_string is None:
            corridors_uploaded = json.loads(corridors_uploaded_string)

        corridors_finished_string = db_mission_data_info['corridors_finished']
        corridors_finished = None
        if not corridors_finished_string is None:
            corridors_finished = json.loads(corridors_finished_string)

        response['response_data'] = {
            'time_sent': db_mission_data_info['time_sent'],
            'time_recorded': db_mission_data_info['time_recorded'],

            'transaction_uuid': db_mission_data_info['transaction_uuid'],

            'start_intersection': db_mission_data_info['start_intersection'],
            'last_uploaded_intersection': db_mission_data_info['last_uploaded_intersection'],
            'last_mission_intersection': db_mission_data_info['last_mission_intersection'],

            'land_after_mission_finished': strtobool(db_mission_data_info['land_after_mission_finished']),

            'corridors_pending': corridors_pending,
            'corridors_approved': corridors_approved,
            'corridors_uploaded': corridors_uploaded,
            'corridors_finished': corridors_finished
        }

    return jsonify(response)


@bp.route('request_clearance')
def ask_request_clearance():
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
    data = payload.get('data')

    response = check_argument_not_null(response, drone_id, 'drone_id')
    response = check_argument_not_null(response, data_type, 'data_type')
    response = check_argument_not_null(response, data, 'data')

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    if not data_type == 'request_clearance':
        response = add_error_to_response(response,
                                         1,
                                         "'data_type' must be 'request_clearance'.",
                                         False)

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    # We want to request to fly through the corridor to an intersection
    corridor_id = data.get('corridor')
    dest_intersection_id = data.get('dest_intersection')

    response = check_argument_not_null(response, corridor_id, 'corridor')
    response = check_argument_not_null(
        response, dest_intersection_id, 'dest_intersection')

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

    # Check if intersection with given id exists
    db_intersection_info = db.execute(
        'SELECT id FROM intersections WHERE id = ?', (dest_intersection_id,)).fetchone()
    if db_intersection_info is None:
        response = add_error_to_response(
            response,
            1,
            f'Intersection with id "{dest_intersection_id}" not found.',
            False
        )

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    # Check if corridor with given id exists
    db_corridor_info = db.execute(
        'SELECT * FROM corridors WHERE id = ?', (corridor_id,)).fetchone()
    if db_corridor_info is None:
        response = add_error_to_response(
            response,
            1,
            f'Corridor with id "{corridor_id}" not found.',
            False
        )
    elif db_corridor_info['intersection_a'] != dest_intersection_id and db_corridor_info['intersection_b'] != dest_intersection_id:
        response = add_error_to_response(
            response,
            1,
            f'Intersection not connected to specified corridor.',
            False
        )

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)
    
    response = check_and_update_infrastructure_locks(response, db)

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    corridor_already_locked = False
    intersection_already_locked = False

    # Check if corridor is locked by another drone
    db_locked_corridor_info = db.execute(
        'SELECT * FROM locked_corridors WHERE corridor_id = ?', (corridor_id,)).fetchone()
    if not db_locked_corridor_info is None:
        if not db_locked_corridor_info['drone_id'] == drone_id:
            corridor_already_locked = True

            response = add_warning_to_response(
                response,
                1,
                'Corridor already locked.'
            )

    # Check if dest_intersection is locked by another drone
    db_locked_intersection_info = db.execute(
        'SELECT * FROM locked_intersections WHERE intersection_id = ?', (dest_intersection_id,)).fetchone()
    if not db_locked_intersection_info is None:
        if not db_locked_intersection_info['drone_id'] == drone_id:
            intersection_already_locked = True

            response = add_warning_to_response(
                response,
                1,
                'Intersection already locked.'
            )

    response['response_data'] = {
        'corridor': corridor_id,
        'dest_intersection': dest_intersection_id,
        'cleared': False
    }
    if corridor_already_locked or intersection_already_locked:
        response['response_data']['cleared'] = False
        return jsonify(response)

    # Lock corridor and intersection
    try:
        db.execute("""
            INSERT INTO locked_intersections(
                intersection_id, drone_id
            ) VALUES (
                ?, ?
            ) ON CONFLICT(intersection_id) DO UPDATE SET
            intersection_id = ?,
            drone_id = ?
            """, (dest_intersection_id, drone_id, dest_intersection_id, drone_id,)
        )

        db.execute("""
            INSERT INTO locked_corridors(
                corridor_id, drone_id
            ) VALUES (
                ?, ?
            ) ON CONFLICT(corridor_id) DO UPDATE SET
            corridor_id = ?,
            drone_id = ?
            """, (corridor_id, drone_id, corridor_id, drone_id,)
        )

        db.commit()

        response['response_data']['cleared'] = True
    except db.IntegrityError:
        response = add_error_to_response(
            response,
            1,
            'Internal server error: IntegrityError while accessing the database.',
            False
        )

    return jsonify(response)


@bp.route('request_flightpath')
def ask_request_flightpath():
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
    data = payload.get('data')

    response = check_argument_not_null(response, drone_id, 'drone_id')
    response = check_argument_not_null(response, data_type, 'data_type')
    response = check_argument_not_null(response, data, 'data')

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    if not data_type == 'request_flightpath':
        response = add_error_to_response(response,
                                         1,
                                         "'data_type' must be 'request_flightpath'.",
                                         False)

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    dest_intersection_id = data.get('dest_intersection')

    response = check_argument_not_null(
        response, dest_intersection_id, 'dest_intersection')

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

    # Check if intersection with given id exists
    db_intersection_info = db.execute(
        'SELECT id FROM intersections WHERE id = ?', (dest_intersection_id,)).fetchone()
    if db_intersection_info is None:
        response = add_error_to_response(
            response,
            1,
            f'Intersection with id "{dest_intersection_id}" not found.',
            False
        )

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    # Get (latest) coordinates of the drone
    # (TODO: Check if last dataset is recent (only a few seconds ago) -
    # otherwise request it)
    db_drone_coordinates = db.execute("""
        SELECT gps_lat, gps_lon
        FROM aircraft_location
        WHERE drone_id = ?
          AND gps_valid = true
        ORDER BY time_recorded DESC
        LIMIT 1
        """, (drone_id,)).fetchone()
    if db_drone_coordinates is None:
        response = add_error_to_response(
            response,
            1,
            f'Drone has no recent aircraft_location data.',
            False
        )

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)
    
    response = check_and_update_infrastructure_locks(response, db)

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)
    
    # Check if destination intersection is currently locked by other drone
    db_tmp_locked_dest_int = db.execute("""
        SELECT *
        FROM locked_intersections
        WHERE intersection_id = ?
          AND drone_id != ?
    """, (dest_intersection_id, drone_id)).fetchone()

    if not db_tmp_locked_dest_int is None:
        response = add_error_to_response(
            response,
            1,
            'Destination intersection is already locked by another drone.',
            False
        )

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    # Get nearest intersection
    # This SQL query was generously provided by GPT-4 and uses the Haversine
    # formula to calculate the distance between two points on a sphere.
    # (TODO: Check destination < 5m)
    db.create_function("acos", 1, math.acos)
    db.create_function("cos", 1, math.cos)
    db.create_function("sin", 1, math.sin)
    db.create_function("radians", 1, math.radians)

    query = """
        WITH distances AS (
        SELECT
            id,
            (
            6371 * acos(
                cos(radians(?)) *
                cos(radians(gps_lat)) *
                cos(radians(gps_lon) - radians(?)) +
                sin(radians(?)) *
                sin(radians(gps_lat))
            )
            ) AS distance
        FROM
            intersections
        )
        SELECT
        id
        FROM
        distances
        ORDER BY
        distance ASC
        LIMIT 1;
    """

    # Execute the query with the drone's GPS coordinates as parameters
    cursor = db.execute(
        query, (db_drone_coordinates['gps_lat'], db_drone_coordinates['gps_lon'], db_drone_coordinates['gps_lat']))

    # Fetch the result and print the nearest intersection id
    nearest_intersection = cursor.fetchone()
    if not nearest_intersection:
        response = add_error_to_response(
            response,
            1,
            f'No (valid) intersection found to be used as start_intersection.',
            False
        )

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)
    
    start_intersection_id = nearest_intersection[0]


    db_intersections = db.execute("""
        SELECT id, gps_lat, gps_lon
        FROM intersections
        WHERE id NOT IN (
            SELECT intersection_id
            FROM locked_intersections
            WHERE drone_id != ?
        )
    """, (drone_id,)).fetchall()

    G = nx.Graph()

    # Add intersections as nodes
    for row in db_intersections:
        intersection_id = row[0]
        G.add_node(intersection_id)

    # Add corridors as edges
    query = """
    SELECT
        id,
        intersection_a,
        intersection_b
    FROM
        corridors
    WHERE
        id NOT IN (
            SELECT corridor_id
            FROM locked_corridors
            WHERE drone_id != ?
        )
        AND (
            intersection_a NOT IN (
                SELECT intersection_id
                FROM locked_intersections
                WHERE drone_id != ?
            )
        )
        AND (
            intersection_b NOT IN (
                SELECT intersection_id
                FROM locked_intersections
                WHERE drone_id != ?
            )
        )
    """
    cursor = db.execute(query, (drone_id, drone_id, drone_id))
    
    for row in cursor:
        corridor_id, intersection_a, intersection_b = row

        lat_a = None
        lon_a = None

        lat_b = None
        lon_b = None

        for intersection in db_intersections:
            if intersection['id'] == intersection_a:
                lat_a = intersection['gps_lat']
                lon_a = intersection['gps_lon']
            if intersection['id'] == intersection_b:
                lat_b = intersection['gps_lat']
                lon_b = intersection['gps_lon']

        distance = haversine_distance(lat_a, lon_a, lat_b, lon_b)

        G.add_edge(intersection_a, intersection_b, id=corridor_id, weight=distance)

    # Find the shortest path between the start and dest intersection
    path_nodes = []
    path_corridors = []
    try:
        path_nodes = nx.shortest_path(G, start_intersection_id, dest_intersection_id)
        path_corridors = [G.edges[path_nodes[i], path_nodes[i + 1]]['id'] for i in range(len(path_nodes) - 1)]
        
        response['response_data'] = {
            'start_intersection': start_intersection_id,
            'flightpath': path_corridors
        }
    except nx.NetworkXNoPath:
        response = add_warning_to_response(
            response,
            1,
            'No available route found.'
        )
    
    # Lock path
    try:
        db.execute("""
            DELETE FROM locked_corridors
            WHERE drone_id = ?
        """, (drone_id,))

        db.execute("""
            DELETE FROM locked_intersections
            WHERE drone_id = ?
        """, (drone_id,))

        for cor in path_corridors:
            db.execute(f"""
                INSERT INTO locked_corridors (corridor_id, drone_id)
                VALUES (?, ?)
            """, (cor, drone_id))
        
        for i_int in path_nodes:
            db.execute(f"""
                INSERT INTO locked_intersections (intersection_id, drone_id)
                VALUES (?, ?)
            """, (i_int, drone_id))
        
        db.commit()
    except db.IntegrityError:
        response = add_error_to_response(
            response,
            1,
            'Internal server error: IntegrityError while accessing the database.',
            False
        )
        response['response_data'] = None
    
    return jsonify(response)
