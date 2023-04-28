import math
import requests
import time

# This file holds variables and functions that can / will be used by all modules

cchainlink_url = 'http://adds-demo.an-men.de:2001/'


def strtobool(val):
    if isinstance(val, bool):
        return val
    elif isinstance(val, str):
        val = val.strip().lower()
        if val in ["true", "1", "yes", "on"]:
            return True
        elif val in ["false", "0", "no", "off"]:
            return False
    elif isinstance(val, (int, float)):
        return val == True
    else:
        return bool(val)


# This function was provided by GPT-4.
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371000  # Earth radius in meters
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

# This function was provided by GPT-3.5.
def distance_to_vector(vector_end_a_lat, vector_end_a_lon, vector_end_b_lat, vector_end_b_lon, point_lat, point_lon):
    # calculate the haversine distance between the point and each endpoint of the vector
    dist_a = haversine_distance(point_lat, point_lon, vector_end_a_lat, vector_end_a_lon)
    dist_b = haversine_distance(point_lat, point_lon, vector_end_b_lat, vector_end_b_lon)

    # calculate the vector direction and magnitude
    dx = vector_end_b_lon - vector_end_a_lon
    dy = vector_end_b_lat - vector_end_a_lat
    mag = math.sqrt(dx**2 + dy**2)

    # calculate the projection of the point onto the vector
    if mag > 0:
        u = ((point_lon - vector_end_a_lon) * dx + (point_lat - vector_end_a_lat) * dy) / mag**2
        projection_lon = vector_end_a_lon + u * dx
        projection_lat = vector_end_a_lat + u * dy
    else:
        # vector has zero length, so set projection to one of the endpoints
        projection_lon, projection_lat = vector_end_a_lon, vector_end_a_lat

    # calculate the haversine distance between the point and the projected point
    dist_projection = haversine_distance(point_lat, point_lon, projection_lat, projection_lon)

    # if the projected point is outside the range of the vector, use the closest endpoint
    if u < 0:
        return dist_a
    elif u > 1:
        return dist_b
    else:
        return dist_projection


def get_response_template(requesting_values=False, response_data=False):
    response = {
        'executed': True,
        'errors': [],
        'warnings': []
    }

    if requesting_values:
        response['requesting_values'] = []

    if response_data:
        response['response_data'] = None

    return response


def add_error_to_response(response, err_id, err_msg, executed=False):
    response['executed'] = executed
    error = {
        'err_id': err_id,
        'err_msg': err_msg
    }
    response['errors'].append(error)

    return response


def add_warning_to_response(response, warn_id, warn_msg):
    warning = {
        'warn_id': warn_id,
        'warn_msg': warn_msg
    }
    response['warnings'].append(warning)

    return response


def check_argument_not_null(response, argument, argument_name, err_id=-1):
    if argument is None:
        response = add_error_to_response(
            response,
            err_id,
            f'Argument missing: {argument_name}',
            False
        )

    return response


def check_argument_type(response, argument, argument_name, data_type, err_id=-1):
    try:
        if data_type == 'int':
            argument = int(argument)
        elif data_type == 'float':
            argument = float(argument)
        elif data_type == 'boolean':
            argument = strtobool(argument)
    except:
        argument = None
        response = add_error_to_response(
            response,
            err_id,
            f'Could not convert "{argument_name}" to {data_type}.'
        )

    return response, argument


def save_data_in_blockchain(response, chain_uuid, payload):
    transaction_uuid = None

    if chain_uuid is None or chain_uuid == '':
        response = add_error_to_response(
            response,
            -1,
            'The ChainUUID is None. Data was not booked in the blockchain!',
            False
        )
        return response, transaction_uuid

    cchainlink_response = None
    try:
        cchainlink_response = requests.get(
            cchainlink_url + 'book_data?'
            + 'chain_uuid=' + chain_uuid
            + '&payload=' + payload)
    except:
        response = add_error_to_response(
            response,
            -1,
            'Could not reach C-Chain Link. Data was not booked in the blockchain!',
            False
        )

    cchainlink_response_json = None
    if not cchainlink_response is None:
        try:
            cchainlink_response_json = cchainlink_response.json()
        except:
            response = add_error_to_response(
                response,
                -1,
                'Invalid response from C-Chain Link. Data may not have been booked in the blockchain!',
                False
            )

    if not cchainlink_response_json is None:
        try:
            transaction_uuid = cchainlink_response_json['response_data']['transaction_uuid']
        except:
            response = add_error_to_response(
                response,
                -1,
                'Invalid response from C-Chain Link (transaction_uuid not transmitted properly). Data may not have been booked in the blockchain!',
                False
            )

        try:
            for err in cchainlink_response_json.get('errors'):
                response = add_error_to_response(
                    response,
                    err.get('err_id'),
                    'From C-Chain Link: ' + err.get('err_msg')
                )
        except:
            response = add_error_to_response(
                response,
                -1,
                'Invalid response from C-Chain Link (errors not transmitted properly). Data may not have been booked in the blockchain!',
                False
            )

        try:
            for warn in cchainlink_response_json.get('warnings'):
                response = add_warning_to_response(
                    response,
                    warn.get('warn_id'),
                    'From C-Chain Link: ' + warn.get('warn_msg')
                )
        except:
            response = add_error_to_response(
                response,
                -1,
                'Invalid response from C-Chain Link (warnings not transmitted properly). Data may not have been booked in the blockchain!',
                False
            )

    if not cchainlink_response_json is None and not cchainlink_response_json.get('executed'):
        response['executed'] = False

    return response, transaction_uuid


def create_chain_mission(response, drone_id):
    chain_uuid = None

    try:
        cchainlink_response = requests.get(
            cchainlink_url + 'create_chain?'
            + 'name=ADDS-MissionChain-' + drone_id
            + '&description=The Mission Chain for the ADDS drone with id ' + drone_id + '.'
        )

        cchainlink_response_json = cchainlink_response.json()
        try:
            if not cchainlink_response_json['executed']:
                response['executed'] = False

            chain_uuid = cchainlink_response_json['response_data']['chain_uuid']
        except:
            response = add_error_to_response(
                response,
                -1,
                'Invalid response from C-Chain Link. The Mission Chain may not have been created!',
                False
            )

        # Transfer errors from C-Chain Link response
        try:
            for err in cchainlink_response_json.get('errors'):
                response = add_error_to_response(
                    response,
                    err.get('err_id'),
                    'From C-Chain Link: ' + err.get('err_msg')
                )
        except:
            response = add_error_to_response(
                response,
                -1,
                'Invalid response from C-Chain Link (errors not transmitted properly). The Mission Chain may not have been created!',
                False
            )

        # Transfer warnings from C-Chain Link response
        try:
            for warn in cchainlink_response_json.get('warnings'):
                response = add_warning_to_response(
                    response,
                    warn.get('warn_id'),
                    'From C-Chain Link: ' + warn.get('warn_msg')
                )
        except:
            response = add_error_to_response(
                response,
                -1,
                'Invalid response from C-Chain Link (warnings not transmitted properly). The Mission Chain may not have been created!',
                False
            )
    except:
        response = add_error_to_response(
            response,
            -1,
            'Could not reach C-Chain Link. The Mission Chain was not created!',
            False
        )
    
    return response, chain_uuid

def create_chain_blackbox(response, drone_id):
    chain_uuid = None

    try:
        cchainlink_response = requests.get(
            cchainlink_url + 'create_chain?'
            + 'name=ADDS-BlackboxChain-' + drone_id
            + '&description=The Blackbox Chain for the ADDS drone with id ' + drone_id + '.'
        )

        cchainlink_response_json = cchainlink_response.json()
        try:
            if not cchainlink_response_json['executed']:
                response['executed'] = False

            chain_uuid = cchainlink_response_json['response_data']['chain_uuid']
        except:
            response = add_error_to_response(
                response,
                -1,
                'Invalid response from C-Chain Link. The Blackbox Chain may not have been created!',
                False
            )

        # Transfer errors from C-Chain Link response
        try:
            for err in cchainlink_response_json.get('errors'):
                response = add_error_to_response(
                    response,
                    err.get('err_id'),
                    'From C-Chain Link: ' + err.get('err_msg')
                )
        except:
            response = add_error_to_response(
                response,
                -1,
                'Invalid response from C-Chain Link (errors not transmitted properly). The Blackbox Chain may not have been created!',
                False
            )

        # Transfer warnings from C-Chain Link response
        try:
            for warn in cchainlink_response_json.get('warnings'):
                response = add_warning_to_response(
                    response,
                    warn.get('warn_id'),
                    'From C-Chain Link: ' + warn.get('warn_msg')
                )
        except:
            response = add_error_to_response(
                response,
                -1,
                'Invalid response from C-Chain Link (warnings not transmitted properly). The Blackbox Chain may not have been created!',
                False
            )
    except:
        response = add_error_to_response(
            response,
            -1,
            'Could not reach C-Chain Link. The Blackbox Chain was not created!',
            False
        )
    
    return response, chain_uuid


last_infrastructure_locks_check = 0
def check_and_update_infrastructure_locks(response, db):
    global last_infrastructure_locks_check

    if time.time() - last_infrastructure_locks_check > 2:
        last_infrastructure_locks_check = time.time()

        # Get inactive drones that still lock any infrastructure
        db_inactive_locking_drones = db.execute("""
            SELECT drone_id
            FROM (
                SELECT drone_id, MAX(time_recorded) as max_time_recorded
                FROM aircraft_location
                GROUP BY drone_id
            )
            WHERE Datetime(max_time_recorded, 'unixepoch') < Datetime('now', '-10 seconds')
                AND drone_id IN (
                    SELECT drone_id
                    FROM locked_intersections
                UNION
                    SELECT drone_id
                    FROM locked_corridors
                )
        """).fetchall()

        # Delete locks from inactive drones
        try:
            for drone in db_inactive_locking_drones:
                db.execute("""
                    DELETE FROM locked_intersections
                    WHERE drone_id = ?
                """, (drone['drone_id'], ))

                db.execute("""
                    DELETE FROM locked_corridors
                    WHERE drone_id = ?
                """, (drone['drone_id'], ))
            
            db.commit()
        except db.IntegrityError:
            response = add_error_to_response(
                response,
                1,
                'Internal server error: IntegrityError while accessing the database.',
                False
            )

        # Unlock infrastructure of drones currently in a mission
        db_missions = db.execute("""
            SELECT md.drone_id as drone_id,
                   md.corridors_pending as corridors_pending,
                   md.corridors_approved as corridors_approved,
                   md.corridors_uploaded as corridors_uploaded
            FROM mission_data as md
            JOIN (
                SELECT drone_id, MAX(time_recorded) as max_time_recorded
                FROM mission_data
                GROUP BY drone_id
            ) as latest
              ON md.drone_id = latest.drone_id
             AND md.time_recorded = latest.max_time_recorded
        """).fetchall()

        for mission in db_missions:
            drone_id = mission['drone_id']
            corridor_ids_pending = mission['corridors_pending']
            corridor_ids_approved = mission['corridors_approved']
            corridor_ids_uploaded = mission['corridors_uploaded']

            corridor_ids_to_keep_locked = corridor_ids_uploaded + corridor_ids_approved + corridor_ids_pending

            db_drone_location = db.execute("""
                SELECT gps_lat, gps_lon
                FROM aircraft_location
                WHERE drone_id = ?
                ORDER BY time_recorded DESC
            """, (drone_id,)).fetchone()

            # Go through uploaded in reverse
            unlock_corridors = False
            for cor_id in reversed(corridor_ids_uploaded):
                if not unlock_corridors:
                    db_cor = db.execute("""
                        SELECT id, intersection_a, intersection_b
                        FROM corridors
                        WHERE id = ?
                    """, (cor_id,)).fetchone()
                    # TODO: Check if result is not None

                    db_cor_ints = db.execute("""
                        SELECT gps_lat, gps_lon
                        FROM intersections
                        WHERE id = ?
                        OR id = ?
                    """, (db_cor['intersection_a'], db_cor['intersection_b'])).fetchall()
                    # TODO: Check if result has two datasets (for both intersections)

                    distance_to_corridor = distance_to_vector(db_cor_ints[0]['gps_lat'], db_cor_ints[0]['gps_lon'],
                                                                db_cor_ints[1]['gps_lat'], db_cor_ints[1]['gps_lon'],
                                                                db_drone_location['gps_lat'], db_drone_location['gps_lon'])

                    if distance_to_corridor <= 2:
                        # Drone is currently flying on this corridor. We can
                        # unlock all previous corridors.
                        unlock_corridors = True
                else:
                    corridor_ids_to_keep_locked.remove(cor_id)

            try:
                db.execute(f"""
                    DELETE FROM locked_intersections
                    WHERE drone_id = ?
                      AND intersection_id NOT IN (
                        SELECT intersection_a, intersection_b
                        FROM (
                            SELECT *
                            FROM corridors
                            WHERE id IN ({','.join(['?']*len(corridor_ids_to_keep_locked))})
                        ) cors
                        LEFT JOIN intersections
                        ON intersections.id = cors.intersection_a
                        OR intersections.id = cors.intersection_b
                    )
                """, (drone_id, *corridor_ids_to_keep_locked,))

                db.execute(f"""
                    DELETE FROM locked_corridors
                    WHERE drone_id = ?
                    AND corridor_id NOT IN ({','.join(['?']*len(corridor_ids_to_keep_locked))})
                """, (drone_id, *corridor_ids_to_keep_locked,))
            except db.IntegrityError:
                response = add_error_to_response(
                    response,
                    1,
                    'Internal server error: IntegrityError while accessing the database.',
                    False
                )

        # TODO: Lock intersections near drones that are not in a mission
    
    return response
