# ADDS-TrafficControl
The central part of the Traffic System running on the main server.

**Initialize database**

This will set up the sqlite database. If it already exists, it will be
overwritten.

```bash
flask --app flaskr init-db
```

**Run**

```bash
flask --app flaskr/ --debug run
```

## API

### Overview

**TELL**

- [x] /api/tell/aircraft_location
- [x] /api/tell/aircraft_power
- [ ] /api/tell/my_health
- [x] /api/tell/register
- [x] /api/tell/deregister
- [x] /api/tell/activate_drone
- [x] /api/tell/deactivate_drone

**ASK**

- [ ] /api/ask/get_drone_info
- [ ] /api/ask/request_flight_plan
- [ ] /api/ask/request_clearance

**INFRASTRUCTURE**

- [x] /api/infrastructure/add_intersection
- [x] /api/infrastructure/remove_intersection
- [x] /api/infrastructute/get_intersection_info
- [x] /api/infrastructure/add_corridor
- [x] /api/infrastructure/remove_corridor
- [x] /api/infrastructure/get_corridor_info

### Structure of the payload

The data sent to Traffic Control can be transmitted by GET or POST. The data
is packaged inside a JSON string with the following format:

```json
{
    "drone_id": <drone_id>,
    "data_type": <data_type>,
    "data": {
        
    }
}
```

In the sections below the `data_type` and `data` fields are specified per
category.

### Structure of return message

The server returns a json string with the following elements.

| FIELD             | REQ / OPT | VALUES                                                |
|-------------------|-----------|-------------------------------------------------------|
| executed          | required  | `'yes'` \| `'no'` \| `'partially'`                    |
| errors            | required  | `[ {err_id: <err_id>, err_msg: <err_msg>}, ... ]`     |
| warnings          | required  | `[ {warn_id: <warn_id>, warn_msg: <warn_msg>}, ... ]` |
| requesting_values | optional  | `[ <value_id>, ... ]`                                 |
| response_data     | optional  |                                                       |

- `<err_msg>` and `<warn_msg>` are just for human visualisation. The value does
  not matter in case of functionality.
- `<value_id>` is the id of the set of values requested by the server. It has
  the same name as the api call: `/api/tell/<value_id>`

### TELL

#### /api/tell/aircraft_location

The drone can send information about the current location, heading and speed.

The `data_type` is `aircraft_location`.

| FIELD                    | TYPE    | REQ / OPT | INFORMATION                                                |
|--------------------------|---------|-----------|------------------------------------------------------------|
| gps_signal_level         | int     | required  | [0;5]                                                      |
| gps_satellites_connected | int     | required  | [0;X]                                                      |
| gps_valid                | boolean | required  | Says whether one can trust the gps_lat and gps_lon values. |
| gps_lat                  | float   | required  | GPS latitude.                                              |
| gps_lon                  | float   | required  | GPS longitude.                                             |
| altitude                 | float   | required  | In meters above take-off point.                            |
| velocity_x               | float   | required  | In meters / second.                                        |
| velocity_y               | float   | required  | In meters / second.                                        |
| velocity_z               | float   | required  | In meters / second.                                        |
| pitch                    | float   | required  | In deg: [-180;180].                                        |
| yaw                      | float   | required  | In deg: [-180;180].                                        |
| roll                     | float   | required  | In deg: [-180;180].                                        |

<details><summary>Sample payload</summary><p>

```json
{
    "drone_id": "demo_drone",
    "data_type": "aircraft_location",
    "data": {
        "gps_signal_level": 5,
        "gps_satellites_connected": 9,
        "gps_valid": "true",
        "gps_lat": 48.047341,
        "gps_lon": 11.654751,
        "altitude": 42,
        "velocity_x": 3.7,
        "velocity_y": 5.0,
        "velocity_z": 0.0,
        "pitch": -20.0,
        "yaw": 0.0,
        "roll": 60.0
    }
}
```

</p></details><br>

#### /api/tell/aircraft_power

The drone can send information about the battery state of charge and remaining
flight time and radius.

The `data_type` is `aircraft_power`.

| FIELD                     | TYPE  | REQ / OPT | INFORMATION                         |
|---------------------------|-------|-----------|-------------------------------------|
| battery_remaining         | int   | required  | Battery capacity remaining. In mAh. |
| battery_remaining_percent | int   | required  | Battery capacity remaining. In %.   |
| remaining_flight_time     | int   | required  | In seconds.                         |
| remaining_flight_radius   | float | required  | In meters.                          |

<details><summary>Sample payload</summary><p>

```json
{
    "drone_id": "demo_drone",
    "data_type": "aircraft_power",
    "data": {
        "battery_remaining": 4500,
        "battery_remaining_percent": 42,
        "remaining_flight_time": 720,
        "remaining_flight_radius": 4530.2
    }
}
```

</p></details><br>

#### /api/tell/register_drone

A drone can be registered. Once a drone is registered, it can "tell data" and be
activated.

| FIELD        | TYPE       | REQ / OPT    |
|--------------|------------|--------------|
| **drone_id** | **string** | **required** |

#### /api/tell/deregister_drone

A drone can be deregistered. Once a drone is deregistered, it cannot be used
anymore. This will delete a drone from the system.

| FIELD        | TYPE       | REQ / OPT    |
|--------------|------------|--------------|
| **drone_id** | **string** | **required** |

#### /api/tell/activate_drone

A drone can be activated. Once a drone is active, it is open for jobs and ready
to be used.

| FIELD        | TYPE       | REQ / OPT    |
|--------------|------------|--------------|
| **drone_id** | **string** | **required** |

#### /api/tell/deactivate_drone

A drone can be deactivated. Once a drone is deactivated, it is not open for jobs
and cannot be used anymore.

| FIELD        | TYPE       | REQ / OPT    |
|--------------|------------|--------------|
| **drone_id** | **string** | **required** |

### ASK

#### /api/ask/get_drone_info

One can request information about a drone. It will contain all information that
is currently known.

| FIELD    | REQ / OPT |
|----------|-----------|
| drone_id | required  |

The `response_data` field of the response will contain the following elements:

```
<drone_id>: {
    'gps_lat':         { 'age': <age>, 'data': <gps_lat> },
    'gps_lon':         { 'age': <age>, 'data': <gps_lon> },
    'height':          { 'age': <age>, 'data': <height> },
    'heading':         { 'age': <age>, 'data': <heading> },
    'air_speed':       { 'age': <age>, 'data': <air_speed> },
    'ground_speed':    { 'age': <age>, 'data': <ground_speed> },
    'vertical_speed':  { 'age': <age>, 'data': <vertical_speed> },
    'flightplan': { 'age': <age>, 'data': [
        {
            coordinates: <coord>,
            height: <height>,
            heading: <heading>
        },
        ...
    ] },
    'health':  { 'age': <age>, 'data': <health> },
    'battery_soc':     { 'age': <age>, 'data': <battery_soc> },
    'rem_flight_time': { 'age': <age>, 'data': <rem_flight_time> }
},
...
```

#### /api/ask/request_flight_plan

A drone can request a flight plan to a destination.

| FIELD       | REQ / OPT |
|-------------|-----------|
| drone_id    | required  |
| destination | required  |

The `requesting_values` field in the response may contain `here_i_am` if the
last known location may not be valid (e.g. last update too long ago).

#### /api/ask/request_clearance

A drone can requets clearance to enter the next corridor. The drone wants to
enter the corridor at intersection A and fly towards intersection B.

| FIELD          | REQ / OPT |
|----------------|-----------|
| drone_id       | required  |
| intersection_a | required  |
| intersection_b | required  |

### INFRASTRUCTURE

#### /api/infrastructure/add_intersection

A system administrator can add a new intersection

| FIELD           | REQ / OPT |
|-----------------|-----------|
| intersection_id | required  |
| gps_lat         | required  |
| gps_lon         | required  |
| height          | required  |

#### /api/infrastructure/remove_intersection

A system administrator can delete an intersection

| FIELD           | REQ / OPT |
|-----------------|-----------|
| intersection_id | required  |

#### /api/infrastructure/get_intersection_info

Get information about a / all intersection(s).

| FIELD           | REQ / OPT | INFO                                                    |
|-----------------|-----------|---------------------------------------------------------|
| intersection_id | required  | Set to `all` to get information about all intersections |

The `response_data` field of the response will contain the following elements:

```
'intersection_id': <id>,
'gps_lat': <gps_lat>,
'gps_lon': <gps_lon>,
'height': <height>
```

or

```
<intersection_id>: {
    'intersection_id': <id>,
    'gps_lat': <gps_lat>,
    'gps_lon': <gps_lon>,
    'height': <height>
},
...
```

#### /api/infrastructure/add_corridor

A system administrator can add a new corridor.

| FIELD          | REQ / OPT |
|----------------|-----------|
| corridor_id    | required  |
| intersection_a | required  |
| intersection_b | required  |

#### /api/infrastructure/remove_corridor

A system administrator can delete a corridor.

| FIELD       | REQ / OPT |
|-------------|-----------|
| corridor_id | required  |

#### /api/infrastructure/get_corridor_info

Get information about a / all corridor(s).

| FIELD       | REQ / OPT | INFO                                                |
|-------------|-----------|-----------------------------------------------------|
| corridor_id | required  | Set to `all` to get information about all corridors |

The `response_data` field of the response will contain the following elements:

```
'corridor_id': <corridor_id>,
'intersection_a': <intersection_a>,
'intersection_b': <intersection_b>
```

or

```
<corridor_id>: {
    'corridor_id': <corridor_id>,
    'intersection_a': <intersection_a>,
    'intersection_b': <intersection_b>
},
...
```
