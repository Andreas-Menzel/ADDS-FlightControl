import functools

from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

# Import own files
from functions_collection import *


bp = Blueprint('infrastructure', __name__, url_prefix='/infrastructure')


@bp.route('/add_intersection')
def add_intersection():
    response = get_response_template()

    intersection_id = request.values.get('intersection_id')
    coordinates_lat = request.values.get('coordinates_lat')
    coordinates_lon = request.values.get('coordinates_lon')
    height          = request.values.get('height')
    
    # Check if all required values were given
    response = check_argument_not_null(response, intersection_id, 'intersection_id')
    response = check_argument_not_null(response, coordinates_lat, 'coordinates_lat')
    response = check_argument_not_null(response, coordinates_lon, 'coordinates_lon')
    response = check_argument_not_null(response, height, 'height')    
    
    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    db = get_db()

    # Check if intersection with given id already exists
    db_intersection_info = db.execute('SELECT * FROM intersections WHERE id = ?', (intersection_id,)).fetchone()
    if not db_intersection_info is None:
        response = add_error_to_response(
            response,
            1,
            f'An intersection with the id "{intersection_id}" already exists.',
            False
        )

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    try:
        db.execute("""
            INSERT INTO intersections(id, coordinates_lat, coordinates_lon, height)
            VALUES(?, ?, ?, ?)
            """, (intersection_id, coordinates_lat, coordinates_lon, height,))

        db.commit()
    except db.IntegrityError:
        response = add_error_to_response(
            response,
            1,
            'Internal server error: IntegrityError while accessing the database',
            False
        )

    return jsonify(response)


@bp.route('/remove_intersection')
def remove_intersection():
    response = get_response_template()

    intersection_id = request.values.get('intersection_id')
    
    # Check if all required values were given
    response = check_argument_not_null(response, intersection_id, 'intersection_id')
    
    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    db = get_db()

    # Check if no corridor is connected to this intersection
    db_corridor_connecting_info = db.execute("""
        SELECT id, intersection_a, intersection_b
        FROM corridors
        WHERE intersection_a = ? OR intersection_b = ?
        """, (intersection_id, intersection_id,)).fetchall()
    if not db_corridor_connecting_info == []:
        for corridor in db_corridor_connecting_info:
            add_error_to_response(
                response,
                1,
                f'The corridor with id "{corridor["id"]}" is still connected to this intersection.',
                False
            )

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    # Check if intersection with given id exists
    db_intersection_info = db.execute('SELECT id FROM intersections WHERE id = ?', (intersection_id,)).fetchone()
    if not db_intersection_info is None:
        try:
            db.execute('DELETE FROM intersections WHERE id = ?', (intersection_id,))

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
            f'An intersection with the id "{intersection_id}" does not exist.'
        )

    return jsonify(response)


@bp.route('/add_corridor')
def add_corridor():
    response = get_response_template()

    corridor_id    = request.values.get('corridor_id')
    intersection_a = request.values.get('intersection_a')
    intersection_b = request.values.get('intersection_b')
    
    # Check if all required values were given
    response = check_argument_not_null(response, corridor_id, 'corridor_id')
    response = check_argument_not_null(response, intersection_a, 'intersection_a')
    response = check_argument_not_null(response, intersection_b, 'intersection_b')
    
    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    db = get_db()

    # Check if intersection_a exists
    db_intersection_a = db.execute('SELECT id FROM intersections WHERE id = ?', (intersection_a,)).fetchone()
    if db_intersection_a is None:
        response = add_error_to_response(
            response,
            1,
            f'The connected intersection_a with id "{intersection_a}" does not exist.',
            False
        )

    # Check if intersection_b exists
    db_intersection_b = db.execute('SELECT id FROM intersections WHERE id = ?', (intersection_b,)).fetchone()
    if db_intersection_b is None:
        response = add_error_to_response(
            response,
            1,
            f'The connected intersection_b with id "{intersection_b}" does not exist.',
            False
        )

    # Check if a corridor with given id already exists
    db_corridor_info = db.execute('SELECT id FROM corridors WHERE id = ?', (corridor_id,)).fetchone()
    if not db_corridor_info is None:
        response = add_error_to_response(
            response,
            1,
            f'A corridor with the id "{corridor_id}" already exists.',
            False
        )
    
    # Check if a corridor connecting the intersection a and b already exists
    db_corridor_connecting_info = db.execute("""
        SELECT id
        FROM corridors
        WHERE (intersection_a = ? AND intersection_b = ?)
           OR (intersection_b = ? AND intersection_a = ?)
        """, (intersection_a, intersection_b, intersection_a, intersection_b,)).fetchone()
    if not db_corridor_connecting_info is None:
        response = add_error_to_response(
            response,
            1,
            f'The corridor with id "{db_corridor_connecting_info["id"]}" already connects the intersections with ids "{intersection_a}" and "{intersection_b}".',
            False
        )

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    try:
        db.execute("""
            INSERT INTO corridors(id, intersection_a, intersection_b)
            VALUES(?, ?, ?)
            """, (corridor_id, intersection_a, intersection_b,))

        db.commit()
    except db.IntegrityError:
        response = add_error_to_response(
            response,
            1,
            'Internal server error: IntegrityError while accessing the database',
            False
        )

    return jsonify(response)


@bp.route('/remove_corridor')
def remove_corridor():
    response = get_response_template()

    corridor_id = request.values.get('corridor_id')
    
    # Check if all required values were given
    response = check_argument_not_null(response, corridor_id, 'corridor_id')
    
    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    db = get_db()

    # Check if corridor with given id exists
    db_corridor_info = db.execute('SELECT id FROM corridors WHERE id = ?', (corridor_id,)).fetchone()
    if not db_corridor_info is None:
        try:
            db.execute('DELETE FROM corridors WHERE id = ?', (corridor_id,))

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
            f'A corridor with the id "{corridor_id}" does not exist.'
        )

    return jsonify(response)
