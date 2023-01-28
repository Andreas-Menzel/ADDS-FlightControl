# ADDS-TrafficSystem-Central
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

- [x] /api/tell/here_i_am
- [ ] /api/tell/here_i_go
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

#### /api/tell/here_i_am

The drone can send information about the current location, heading and speed.

| FIELD                      | TYPE        | REQ / OPT    | INFORMATION        |
|----------------------------|-------------|--------------|--------------------|
| **drone_id**               | **string**  | **required** |                    |
| *gps_signal_level*         | *int*       | *optional*   | DJI drone: 0-5     |
| *gps_satellites_connected* | *int*       | *optional*   |                    |
| **gps_valid**              | **boolean** | **required** |                    |
| **gps_lat**                | **float**   | **required** |                    |
| **gps_lon**                | **float**   | **required** |                    |
| **altitude**               | **float**   | **required** | In meters          |
| *pitch*                    | *float*     | *optional*   | In deg: -180 - 180 |
| *yaw*                      | *float*     | *optional*   | In deg: -180 - 180 |
| *roll*                     | *float*     | *optional*   | In deg: -180 - 180 |

#### /api/tell/here_i_go

The drone can send information about the planned flight path.

| FIELD     | REQ / OPT | VALUES                                                                   |
|-----------|-----------|--------------------------------------------------------------------------|
| drone_id  | required  |                                                                          |
| waypoints | required  | `[ { coordinates: <coord>, height: <height>, heading: <heading>}, ... ]` |

#### /api/tell/my_health

The drone can send information about its current health and status.

| FIELD           | REQ / OPT | VALUES                  |
|-----------------|-----------|-------------------------|
| drone_id        | required  |                         |
| health          | required  | `'ok'` \| `'emergency'` |
| battery_soc     | required  |                         |
| rem_flight_time | optional  |                         |

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
    'coordinates_lat': { 'age': <age>, 'data': <coordinates> },
    'coordinates_lon': { 'age': <age>, 'data': <coordinates> },
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
| coordinates_lat | required  |
| coordinates_lon | required  |
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
'coordinates_lat': <coordinates_lat>,
'coordinates_lon': <coordinates_lon>,
'height': <height>
```

or

```
<intersection_id>: {
    'intersection_id': <id>,
    'coordinates_lat': <coordinates_lat>,
    'coordinates_lon': <coordinates_lon>,
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
