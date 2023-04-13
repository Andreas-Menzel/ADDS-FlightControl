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


@bp.route('intersection_location')
def tell_intersection_location():
    response = get_response_template()

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
    # time_sent is not needed here
    data = payload.get('data')

    response = check_argument_not_null(
        response, intersection_id, 'intersection_id')
    response = check_argument_not_null(response, data_type, 'data_type')
    response = check_argument_not_null(response, data, 'data')

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

    gps_lat = data.get('gps_lat')
    gps_lon = data.get('gps_lon')
    altitude = data.get('altitude')

    response = check_argument_not_null(response, gps_lat, 'gps_lat')
    response = check_argument_not_null(response, gps_lon, 'gps_lon')
    response = check_argument_not_null(response, altitude, 'altitude')

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    # Convert variables to correct type
    response, gps_lat = check_argument_type(
        response, gps_lat, 'gps_lat', 'float')
    response, gps_lon = check_argument_type(
        response, gps_lon, 'gps_lon', 'float')
    response, altitude = check_argument_type(
        response, altitude, 'altitude', 'float')

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    db = get_db()

    try:
        db.execute("""
            INSERT INTO intersections(
                id, gps_lat, gps_lon, altitude
            ) VALUES (
                ?, ?, ?, ?
            )
            ON CONFLICT(id) DO UPDATE SET
            gps_lat = ?,
            gps_lon = ?,
            altitude = ?
            """, (intersection_id, gps_lat, gps_lon, altitude, gps_lat, gps_lon, altitude,)
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


@bp.route('delete_intersection')
def tell_delete_intersection():
    response = get_response_template()

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
    # time_sent is not needed here
    data_type = payload.get('data_type')
    # data is not needed here

    response = check_argument_not_null(
        response, intersection_id, 'intersection_id')
    response = check_argument_not_null(response, data_type, 'data_type')

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    if not data_type == 'delete_intersection':
        response = add_error_to_response(response,
                                         1,
                                         "'data_type' must be 'delete_intersection'.",
                                         False)

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    db = get_db()

    # Check that intersection is not part of a corridor
    tmp_db_corridor_ids = db.execute("""
        SELECT id
        FROM corridors
        WHERE intersection_a = ?
           OR intersection_b = ?
        """, (intersection_id, intersection_id,)).fetchall()

    if not tmp_db_corridor_ids is None:
        for cor in tmp_db_corridor_ids:
            cor_id = cor['id']
            response = add_error_to_response(
                response,
                -1,
                'Cannot delete intersection. Is still part of corridor with id "' + cor_id + '".',
                False
            )

    if not response['executed']:
        return jsonify(response)

    # Delete intersection
    try:
        db.execute("""
            DELETE FROM intersections
            WHERE id = ?
            """, (intersection_id,)
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


@bp.route('corridor_location')
def tell_corridor_location():
    response = get_response_template()

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
    # time_sent is not needed here
    data_type = payload.get('data_type')
    data = payload.get('data')

    response = check_argument_not_null(response, corridor_id, 'corridor_id')
    response = check_argument_not_null(response, data_type, 'data_type')
    response = check_argument_not_null(response, data, 'data')

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

    intersection_a = data.get('intersection_a')
    intersection_b = data.get('intersection_b')

    response = check_argument_not_null(
        response, intersection_a, 'intersection_a')
    response = check_argument_not_null(
        response, intersection_b, 'intersection_b')

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    if intersection_a == intersection_b:
        response = add_error_to_response(
            response,
            -1,
            'Intersections A and B must not be the same!',
            False
        )

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    db = get_db()

    # Check if intersection_a exists
    tmp_db_intersection_a_id = db.execute("""
        SELECT id
        FROM intersections
        WHERE id = ?
        """, (intersection_a,)).fetchone()
    if tmp_db_intersection_a_id is None:
        response = add_error_to_response(
            response,
            1,
            f'Intersection A with id "{intersection_a}" not found.',
            False
        )

    # Check if intersection_b exists
    tmp_db_intersection_b_id = db.execute("""
        SELECT id
        FROM intersections
        WHERE id = ?
        """, (intersection_b,)).fetchone()
    if tmp_db_intersection_b_id is None:
        response = add_error_to_response(
            response,
            1,
            f'Intersection B with id "{intersection_b}" not found.',
            False
        )

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    try:
        db.execute("""
            INSERT INTO corridors(
                id, intersection_a, intersection_b
            ) VALUES (
                ?, ?, ?
            )
            ON CONFLICT(id) DO UPDATE SET
            intersection_a = ?,
            intersection_b = ?
            """, (corridor_id, intersection_a, intersection_b, intersection_a, intersection_b,)
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


@bp.route('delete_corridor')
def tell_delete_corridor():
    response = get_response_template()

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
    # time_sent is not needed here
    data_type = payload.get('data_type')
    # data is not needed here

    response = check_argument_not_null(response, corridor_id, 'corridor_id')
    response = check_argument_not_null(response, data_type, 'data_type')

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    if not data_type == 'delete_corridor':
        response = add_error_to_response(response,
                                         1,
                                         "'data_type' must be 'delete_corridor'.",
                                         False)

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    db = get_db()

    try:
        db.execute("""
            DELETE FROM corridors
            WHERE id = ?
            """, (corridor_id,)
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


@bp.route('aircraft_location')
def tell_aircraft_location():
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
    time_sent = payload.get('time_sent')
    data_type = payload.get('data_type')
    data = payload.get('data')

    response = check_argument_not_null(response, drone_id, 'drone_id')
    response = check_argument_not_null(response, time_sent, 'time_sent')
    response = check_argument_not_null(response, data_type, 'data_type')
    response = check_argument_not_null(response, data, 'data')

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

    time_recorded = data.get('time_recorded')
    gps_signal_level = data.get('gps_signal_level')
    gps_satellites_connected = data.get('gps_satellites_connected')
    gps_valid = data.get('gps_valid')
    gps_lat = data.get('gps_lat')
    gps_lon = data.get('gps_lon')
    altitude = data.get('altitude')
    velocity_x = data.get('velocity_x')
    velocity_y = data.get('velocity_y')
    velocity_z = data.get('velocity_z')
    pitch = data.get('pitch')
    yaw = data.get('yaw')
    roll = data.get('roll')

    response = check_argument_not_null(
        response, time_recorded, 'time_recorded')
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
    response, time_sent = check_argument_type(
        response, time_sent, 'time_sent', 'float')
    response, time_recorded = check_argument_type(
        response, time_recorded, 'time_recorded', 'float')
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

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    db = get_db()

    # Check if drone with given id exists
    tmp_db_drone_info = db.execute("""
        SELECT id, chain_uuid_blackbox
        FROM drones
        WHERE id = ?
        """, (drone_id,)).fetchone()
    if tmp_db_drone_info is None:
        response = add_error_to_response(
            response,
            1,
            f'Drone with id "{drone_id}" not found.',
            False
        )

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    # Save data in blockchain and get transaction_uuid
    response, transaction_uuid = save_data_in_blockchain(
        response, tmp_db_drone_info['chain_uuid_blackbox'], payload_as_json_string)
    response['response_data'] = {}
    response['response_data']['transaction_uuid'] = transaction_uuid

    try:
        db.execute("""
            INSERT INTO aircraft_location(
                time_sent,
                time_recorded,
                transaction_uuid,
                drone_id,
                gps_signal_level,
                gps_satellites_connected,
                gps_valid,
                gps_lat,
                gps_lon,
                altitude,
                velocity_x,
                velocity_y,
                velocity_z,
                pitch,
                yaw,
                roll
            )
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
            """, (time_sent, time_recorded, transaction_uuid, drone_id, gps_signal_level, gps_satellites_connected, gps_valid, gps_lat, gps_lon, altitude, velocity_x, velocity_y, velocity_z, pitch, yaw, roll,)
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


@bp.route('aircraft_power')
def tell_aircraft_power():
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
    time_sent = payload.get('time_sent')
    data_type = payload.get('data_type')
    data = payload.get('data')

    response = check_argument_not_null(response, drone_id, 'drone_id')
    response = check_argument_not_null(response, time_sent, 'time_sent')
    response = check_argument_not_null(response, data_type, 'data_type')
    response = check_argument_not_null(response, data, 'data')

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

    time_recorded = data.get('time_recorded')
    battery_remaining = data.get('battery_remaining')
    battery_remaining_percent = data.get('battery_remaining_percent')
    remaining_flight_time = data.get('remaining_flight_time')
    remaining_flight_radius = data.get('remaining_flight_radius')

    response = check_argument_not_null(
        response, time_recorded, 'time_recorded')
    response = check_argument_not_null(
        response, battery_remaining, 'battery_remaining')
    response = check_argument_not_null(
        response, battery_remaining_percent, 'battery_remaining_percent')
    response = check_argument_not_null(
        response, remaining_flight_time, 'remaining_flight_time')
    response = check_argument_not_null(
        response, remaining_flight_radius, 'remaining_flight_radius')

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    # Convert variables to correct type
    response, time_sent = check_argument_type(
        response, time_sent, 'time_sent', 'float')
    response, time_recorded = check_argument_type(
        response, time_recorded, 'time_recorded', 'float')
    response, battery_remaining = check_argument_type(
        response, battery_remaining, 'battery_remaining', 'int')
    response, battery_remaining_percent = check_argument_type(
        response, battery_remaining_percent, 'battery_remaining_percent', 'int')
    response, remaining_flight_time = check_argument_type(
        response, remaining_flight_time, 'remaining_flight_time', 'int')
    response, remaining_flight_radius = check_argument_type(
        response, remaining_flight_radius, 'remaining_flight_radius', 'float')

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    db = get_db()

    # Check if drone with given id exists
    tmp_db_drone_info = db.execute("""
        SELECT id, chain_uuid_blackbox
        FROM drones
        WHERE id = ?
        """, (drone_id,)).fetchone()
    if tmp_db_drone_info is None:
        response = add_error_to_response(
            response,
            1,
            f'Drone with id "{drone_id}" not found.',
            False
        )

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    # Save data in blockchain and get transaction_uuid
    response, transaction_uuid = save_data_in_blockchain(
        response, tmp_db_drone_info['chain_uuid_blackbox'], payload_as_json_string)
    response['response_data'] = {}
    response['response_data']['transaction_uuid'] = transaction_uuid

    try:
        db.execute("""
            INSERT INTO aircraft_power(
                time_sent,
                time_recorded,
                transaction_uuid,
                drone_id,
                battery_remaining,
                battery_remaining_percent,
                remaining_flight_time,
                remaining_flight_radius
            )
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?
            )
            """, (time_sent, time_recorded, transaction_uuid, drone_id, battery_remaining, battery_remaining_percent, remaining_flight_time, remaining_flight_radius,)
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


@bp.route('flight_data')
def tell_flight_data():
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
    time_sent = payload.get('time_sent')
    data_type = payload.get('data_type')
    data = payload.get('data')

    response = check_argument_not_null(response, drone_id, 'drone_id')
    response = check_argument_not_null(response, time_sent, 'time_sent')
    response = check_argument_not_null(response, data_type, 'data_type')
    response = check_argument_not_null(response, data, 'data')

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

    time_recorded = data.get('time_recorded')

    takeoff_time = data.get('takeoff_time')
    takeoff_gps_valid = data.get('takeoff_gps_valid')
    takeoff_gps_lat = data.get('takeoff_gps_lat')
    takeoff_gps_lon = data.get('takeoff_gps_lon')

    landing_time = data.get('landing_time')
    landing_gps_valid = data.get('landing_gps_valid')
    landing_gps_lat = data.get('landing_gps_lat')
    landing_gps_lon = data.get('landing_gps_lon')

    operation_modes = data.get('operation_modes')

    response = check_argument_not_null(
        response, time_recorded, 'time_recorded')

    response = check_argument_not_null(
        response, takeoff_time, 'takeoff_time')
    response = check_argument_not_null(
        response, takeoff_gps_valid, 'takeoff_gps_valid')
    response = check_argument_not_null(
        response, takeoff_gps_lat, 'takeoff_gps_lat')
    response = check_argument_not_null(
        response, takeoff_gps_lon, 'takeoff_gps_lon')

    response = check_argument_not_null(
        response, landing_time, 'landing_time')
    response = check_argument_not_null(
        response, landing_gps_valid, 'landing_gps_valid')
    response = check_argument_not_null(
        response, landing_gps_lat, 'landing_gps_lat')
    response = check_argument_not_null(
        response, landing_gps_lon, 'landing_gps_lon')

    response = check_argument_not_null(
        response, operation_modes, 'operation_modes')

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    # Convert variables to correct type
    response, time_sent = check_argument_type(
        response, time_sent, 'time_sent', 'float')
    response, time_recorded = check_argument_type(
        response, time_recorded, 'time_recorded', 'float')

    response, takeoff_time = check_argument_type(
        response, takeoff_time, 'takeoff_time', 'int')
    response, takeoff_gps_valid = check_argument_type(
        response, takeoff_gps_valid, 'takeoff_gps_valid', 'boolean')
    response, takeoff_gps_lat = check_argument_type(
        response, takeoff_gps_lat, 'takeoff_gps_lat', 'float')
    response, takeoff_gps_lon = check_argument_type(
        response, takeoff_gps_lon, 'takeoff_gps_lon', 'float')

    response, landing_time = check_argument_type(
        response, landing_time, 'landing_time', 'int')
    response, landing_gps_valid = check_argument_type(
        response, landing_gps_valid, 'landing_gps_valid', 'boolean')
    response, landing_gps_lat = check_argument_type(
        response, landing_gps_lat, 'landing_gps_lat', 'float')
    response, landing_gps_lon = check_argument_type(
        response, landing_gps_lon, 'landing_gps_lon', 'float')

    # TODO: check type of operation_modes: list of strings (?)

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    db = get_db()

    # Check if drone with given id exists
    tmp_db_drone_info = db.execute("""
        SELECT id, chain_uuid_blackbox
        FROM drones
        WHERE id = ?
        """, (drone_id,)).fetchone()
    if tmp_db_drone_info is None:
        response = add_error_to_response(
            response,
            1,
            f'Drone with id "{drone_id}" not found.',
            False
        )

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    # Save data in blockchain and get transaction_uuid
    response, transaction_uuid = save_data_in_blockchain(
        response, tmp_db_drone_info['chain_uuid_blackbox'], payload_as_json_string)
    response['response_data'] = {}
    response['response_data']['transaction_uuid'] = transaction_uuid

    str_operation_modes = json.dumps(operation_modes)
    try:
        db.execute("""
            INSERT INTO flight_data(
                time_sent,
                time_recorded,
                transaction_uuid,
                drone_id,
                takeoff_time,
                takeoff_gps_valid,
                takeoff_gps_lat,
                takeoff_gps_lon,
                landing_time,
                landing_gps_valid,
                landing_gps_lat,
                landing_gps_lon,
                operation_modes
            )
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
            """, (time_sent, time_recorded, transaction_uuid, drone_id, takeoff_time, takeoff_gps_valid, takeoff_gps_lat, takeoff_gps_lon, landing_time, landing_gps_valid, landing_gps_lat, landing_gps_lon, str_operation_modes,)
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
def tell_register_drone():
    response = get_response_template()

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
    # time_sent is not needed here
    data_type = payload.get('data_type')
    data = payload.get('data')

    response = check_argument_not_null(response, drone_id, 'drone_id')
    response = check_argument_not_null(response, data_type, 'data_type')
    response = check_argument_not_null(response, data, 'data')

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    if not data_type == 'register_drone':
        response = add_error_to_response(response,
                                         1,
                                         "'data_type' must be 'register_drone'.",
                                         False)

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    # TODO:
    #crypt_id = data.get('crypt_id')

    # TODO:
    # response = check_argument_not_null(
    #    response, crypt_id, 'crypt_id')

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    # Convert variables to correct type
    # TODO: crypt_id
    # response, takeoff_time = check_argument_type(
    #    response, takeoff_time, 'takeoff_time', 'int')

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    db = get_db()

    is_new_registration = True
    chain_uuid_mission = None
    chain_uuid_blackbox = None

    # Check if drone with given id exists (fully registered or not)
    tmp_db_drone_id = db.execute("""
        SELECT id, chain_uuid_mission, chain_uuid_blackbox
        FROM drones
        WHERE id = ?
        """, (drone_id,)).fetchone()
    if not tmp_db_drone_id is None:
        is_new_registration = False

        if tmp_db_drone_id['chain_uuid_mission'] is None or tmp_db_drone_id['chain_uuid_mission'] == '':
            chain_uuid_mission = None
        else:
            chain_uuid_mission = tmp_db_drone_id['chain_uuid_mission']

        if tmp_db_drone_id['chain_uuid_blackbox'] is None or tmp_db_drone_id['chain_uuid_blackbox'] == '':
            chain_uuid_blackbox = None
        else:
            chain_uuid_blackbox = tmp_db_drone_id['chain_uuid_blackbox']

        if chain_uuid_mission is None or chain_uuid_blackbox is None:
            response = add_warning_to_response(
                response,
                -1,
                'This drone is already (partially?) registered.'
            )

    # Create chains
    if chain_uuid_mission is None:
        response, chain_uuid_mission = create_chain_mission(
            response, drone_id)
    if chain_uuid_blackbox is None:
        response, chain_uuid_blackbox = create_chain_blackbox(
            response, drone_id)

    try:
        if is_new_registration:
            db.execute("""
                INSERT INTO drones (
                    id
                )
                VALUES (
                    ?
                )
            """, (drone_id,)
            )

        db.execute("""
            UPDATE drones
            SET chain_uuid_mission = ?,
                chain_uuid_blackbox = ?
            WHERE id = ?
        """, (chain_uuid_mission, chain_uuid_blackbox, drone_id,)
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


@bp.route('mission_data')
def tell_mission_data():
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
    time_sent = payload.get('time_sent')
    data_type = payload.get('data_type')
    data = payload.get('data')

    response = check_argument_not_null(response, drone_id, 'drone_id')
    response = check_argument_not_null(response, time_sent, 'time_sent')
    response = check_argument_not_null(response, data_type, 'data_type')
    response = check_argument_not_null(response, data, 'data')

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

    time_recorded = data.get('time_recorded')

    start_intersection = data.get('start_intersection')
    last_uploaded_intersection = data.get('last_uploaded_intersection')
    last_mission_intersection = data.get('last_mission_intersection')

    land_after_mission_finished = data.get('land_after_mission_finished')

    corridors_pending = data.get('corridors_pending')
    corridors_approved = data.get('corridors_approved')
    corridors_uploaded = data.get('corridors_uploaded')
    corridors_finished = data.get('corridors_finished')

    response = check_argument_not_null(
        response, time_recorded, 'time_recorded')

    response = check_argument_not_null(
        response, start_intersection, 'start_intersection')
    response = check_argument_not_null(
        response, last_uploaded_intersection, 'last_uploaded_intersection')
    response = check_argument_not_null(
        response, last_mission_intersection, 'last_mission_intersection')

    response = check_argument_not_null(
        response, land_after_mission_finished, 'land_after_mission_finished')

    response = check_argument_not_null(
        response, corridors_pending, 'corridors_pending')
    response = check_argument_not_null(
        response, corridors_approved, 'corridors_approved')
    response = check_argument_not_null(
        response, corridors_uploaded, 'corridors_uploaded')
    response = check_argument_not_null(
        response, corridors_finished, 'corridors_finished')

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    # Convert variables to correct type
    response, time_sent = check_argument_type(
        response, time_sent, 'time_sent', 'float')
    response, time_recorded = check_argument_type(
        response, time_recorded, 'time_recorded', 'float')

    response, land_after_mission_finished = check_argument_type(
        response, land_after_mission_finished, 'land_after_mission_finished', 'boolean')

    # TODO: check type of corridors_pending: list of strings (?)
    # TODO: check type of corridors_approved: list of strings (?)
    # TODO: check type of corridors_uploaded: list of strings (?)
    # TODO: check type of corridors_finished: list of strings (?)

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    db = get_db()

    # Check if drone with given id exists
    tmp_db_drone_info = db.execute("""
        SELECT id, chain_uuid_mission
        FROM drones
        WHERE id = ?
        """, (drone_id,)).fetchone()
    if tmp_db_drone_info is None:
        response = add_error_to_response(
            response,
            1,
            f'Drone with id "{drone_id}" not found.',
            False
        )

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    # Save data in blockchain and get transaction_uuid
    response, transaction_uuid = save_data_in_blockchain(
        response, tmp_db_drone_info['chain_uuid_mission'], payload_as_json_string)
    response['response_data'] = {}
    response['response_data']['transaction_uuid'] = transaction_uuid

    str_corridors_pending = json.dumps(corridors_pending)
    str_corridors_approved = json.dumps(corridors_approved)
    str_corridors_uploaded = json.dumps(corridors_uploaded)
    str_corridors_finished = json.dumps(corridors_finished)
    try:
        db.execute("""
            INSERT INTO mission_data(
                time_sent,
                time_recorded,

                transaction_uuid,
                drone_id,

                start_intersection,
                last_uploaded_intersection,
                last_mission_intersection,

                land_after_mission_finished,

                corridors_pending,
                corridors_approved,
                corridors_uploaded,
                corridors_finished
            )
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
            """, (time_sent, time_recorded,
                  transaction_uuid, drone_id,
                  start_intersection, last_uploaded_intersection, last_mission_intersection,
                  land_after_mission_finished,
                  str_corridors_pending, str_corridors_approved, str_corridors_uploaded, str_corridors_finished,)
        )

        db.commit()
    except db.IntegrityError:
        response = add_error_to_response(
            response,
            1,
            'Internal server error: IntegrityError while accessing the database.',
            False
        )

    all_corridors = corridors_pending + corridors_approved + \
        corridors_uploaded + corridors_finished
    corridor_ids_to_keep_locked = corridors_pending + \
        corridors_approved + corridors_uploaded

    tmp_intersections_info = db.execute(f"""
        SELECT intersections
        FROM (
            
            SELECT intersection_a AS intersections
            FROM corridors
            WHERE id IN ({','.join(['?']*len(corridor_ids_to_keep_locked))})
        UNION
            SELECT intersection_b AS intersections
            FROM corridors
            WHERE id IN ({','.join(['?']*len(corridor_ids_to_keep_locked))})
        )
        """, (*corridor_ids_to_keep_locked, *corridor_ids_to_keep_locked,)).fetchall()

    intersection_ids_to_keep_locked = []
    if not tmp_intersections_info is None:
        intersection_ids_to_keep_locked = [row[0]
                                           for row in tmp_intersections_info]

    # Unlock intersections and corridors that are not needed (any more)
    try:
        db.execute(f"""
            DELETE FROM locked_corridors
            WHERE drone_id = ?
              AND corridor_id NOT IN ({','.join(['?']*len(corridor_ids_to_keep_locked))})
            """, (drone_id, *corridor_ids_to_keep_locked,)
        )

        db.execute(f"""
            DELETE FROM locked_intersections
            WHERE drone_id = ?
              AND intersection_id NOT IN ({','.join(['?']*len(intersection_ids_to_keep_locked))})
            """, (drone_id, *intersection_ids_to_keep_locked,)
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
