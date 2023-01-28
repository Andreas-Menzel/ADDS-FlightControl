# This file holds variables and functions that can / will be used by all modules

# Function copied from "https://github.com/python/cpython/blob/b2076b00710c4366dcfe6cd236e480d68a3c38b7/Lib/distutils/util.py#L308"
def strtobool (val):
    """Convert a string representation of truth to true (1) or false (0).
    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """
    val = val.lower()
    if val in ('y', 'yes', 't', 'true', 'on', '1'):
        return 1
    elif val in ('n', 'no', 'f', 'false', 'off', '0'):
        return 0
    else:
        raise ValueError("invalid truth value %r" % (val,))


def get_response_template(requesting_values = False, response_data = False):
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


def add_error_to_response(response, err_id, err_msg, executed = False):
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


def check_argument_not_null(response, argument, argument_name, err_id = -1):
    if argument is None:
        response = add_error_to_response(
            response,
            err_id,
            f'Argument missing: {argument_name}',
            False
        )
    
    return response


def check_argument_type(response, argument, argument_name, data_type, err_id = -1):
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