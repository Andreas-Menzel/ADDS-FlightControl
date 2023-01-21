# This file holds variables and functions that can / will be used by all modules

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