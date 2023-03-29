import requests

# This file holds variables and functions that can / will be used by all modules

cchainlink_url = 'http://adds-demo.an-men.de:8080/'


# Function copied from "https://github.com/python/cpython/blob/b2076b00710c4366dcfe6cd236e480d68a3c38b7/Lib/distutils/util.py#L308"
def strtobool(val):
    """Convert a string representation of truth to true (1) or false (0).
    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    if isinstance(val, bool):
        return val

    val = val.lower()
    if val in ('y', 'yes', 't', 'true', 'on', '1'):
        return 1
    elif val in ('n', 'no', 'f', 'false', 'off', '0'):
        return 0
    else:
        raise ValueError("invalid truth value %r" % (val,))


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


def save_data_in_blockchain(response, payload):
    transaction_uuid = None

    cchainlink_response = None
    try:
        cchainlink_response = requests.get(
            cchainlink_url + 'book_data?payload=' + payload)
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
