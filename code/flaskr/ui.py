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

    db = get_db()

    # Draw intersections
    db_intersections = db.execute('SELECT * FROM intersections').fetchall()
    for intersection in db_intersections:
        folium.Marker(
            [intersection['gps_lat'], intersection['gps_lon']],
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
                [float(intersection_a['gps_lat']), intersection_a['gps_lon']],
                [intersection_b['gps_lat'], intersection_b['gps_lon']]
            ],
            color='red',
            weight=10,
            opacity=1,
            popup=f'<b>{corridor["id"]}</b>',
            tooltip=f'<b>{corridor["id"]}</b>'
        ).add_to(folium_map)

    # Draw drones
    db_drones = db.execute('SELECT * FROM drones').fetchall()
    for drone in db_drones:
        drone_id = drone["id"]
        lat = drone['gps_lat']
        lon = drone['gps_lon']

        try:
            lat = float(lat)
        except:
            print(f'Could not convert lat: "{lat}"')
            lat = 0

        try:
            print(f'Could not convert lon: "{lon}"')
            lon = float(lon)
        except:
            lon = 0

        folium.Marker(
            [lat, lon],
            popup=f'<b>{drone_id}</b> at {lat} / {lon}',
            tooltip=f'<b>{drone_id}</b>',
            color='orange'
        ).add_to(folium_map)

    return folium_map._repr_html_()


@bp.route('/show_flightpath')
def show_flightplan():
    start_coords = (48.047341, 11.654751)
    folium_map = folium.Map(location=start_coords, zoom_start=18)

    db = get_db()

    db_locations = db.execute('SELECT * FROM aircraft_location WHERE drone_id = "demo_drone"').fetchall()
    lat_old = 0
    lon_old = 0
    for location in db_locations:
        lat_new = location['gps_lat']
        lon_new = location['gps_lon']
        gps_valid = strtobool(location['gps_valid'])

        # Check if has changed and is valid
        if lat_old == lat_new and lon_old == lon_new:
            continue
        if not gps_valid:
            continue

        # Draw line if we have two coordinates
        if not (lat_old == 0 and lon_old == 0):
            folium.PolyLine(
                [
                    [lat_old, lon_old],
                    [lat_new, lon_new]
                ],
                color='red',
                weight=5,
                opacity=1
                #popup=f'<b>{corridor["id"]}</b>',
                #tooltip=f'<b>{corridor["id"]}</b>'
            ).add_to(folium_map)

        lat_old = lat_new
        lon_old = lon_new

    return folium_map._repr_html_()
