import functools

from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

import folium

# Import own files
from functions_collection import *


bp = Blueprint('ui', __name__, url_prefix='/ui')

@bp.route('/')
def send_commands():
    return render_template('ui.html')

@bp.route('/show_infrastructure')
def show_infrastructure():
    start_coords = (48.047341, 11.654751)
    folium_map = folium.Map(location=start_coords, zoom_start=18)

    tooltip = "Click to !"

    db = get_db()

    # Draw intersections
    db_intersections = db.execute('SELECT * FROM intersections').fetchall()
    for intersection in db_intersections:
        folium.Marker(
            [intersection['coordinates_lat'], intersection['coordinates_lon']],
            popup=f'<b>{intersection["id"]}</b>',
            tooltip=f'<b>{intersection["id"]}</b>'
        ).add_to(folium_map)

    # Draw corridors
    db_corridors = db.execute('SELECT * FROM corridors').fetchall()
    for corridor in db_corridors:
        
        intersection_a = None
        intersection_b = None
        for intersection in db_intersections:
            if intersection['id'] == corridor['intersection_a']:
                intersection_a = intersection
            if intersection['id'] == corridor['intersection_b']:
                intersection_b = intersection


        folium.PolyLine(
            [
                [float(intersection_a['coordinates_lat']), intersection_a['coordinates_lon']],
                [intersection_b['coordinates_lat'], intersection_b['coordinates_lon']]
            ],
            color='red',
            weight=10,
            opacity=1,
            popup=f'<b>{corridor["id"]}</b>',
            tooltip=f'<b>{corridor["id"]}</b>'
        ).add_to(folium_map)

    return folium_map._repr_html_()
