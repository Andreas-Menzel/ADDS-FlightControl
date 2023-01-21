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
- [x] /api/tell/my_health
- [x] /api/tell/register
- [x] /api/tell/deregister

- TODO: activate vs register

**ASK**

- [x] /api/ask/get_drone_info
- [ ] /api/ask/request_flight_plan
- [x] /api/ask/request_clearance

**INFRASTRUCTURE**

- [x] /api/infrastructure/add_intersection
- [x] /api/infrastructure/remove_intersection
- [x] /api/infrastructure/add_corridor
- [x] /api/infrastructure/remove_corridor

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

| FIELD           | REQ / OPT | INFORMATION                        |
|-----------------|-----------|------------------------------------|
| drone_id        | required  |                                    |
| coordinates_lat | required  |                                    |
| coordinates_lon | required  |                                    |
| height          | required  | In m                               |
| heading         | required  | In deg; 0:north, 90: east          |
| air_speed       | optional  | In m/s                             |
| ground_speed    | optional  | In m/s                             |
| vertical_speed  | optional  | Speed of ascent or descent. In m/s |

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

#### /api/tell/register

A drone can register itself. Once a drone is registered, it is open for jobs
and ready to be used.

| FIELD    | REQ / OPT |
|----------|-----------|
| drone_id | required  |

#### /api/tell/deregister

A drone can deregister itself. Once a drone is deregistered, it is not open for
jobs and cannot be used anymore.

| FIELD    | REQ / OPT |
|----------|-----------|
| drone_id | required  |

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
