# Documentation - API - ASK

With the ASK interfaces, one can **request information from** Traffic Control.

These interfaces are accessible via `<server_domain>/api/ask/<interface>`.

## Overview

- [Format of the request payload and response](#format-of-the-request-payload-and-response)
- [Interfaces](#interfaces)
    - [intersection_list](#intersection_list)
    - [intersection_location](#intersection_location)
    - [corridor_list](#corridor_list)
    - [corridor_location](#corridor_location)
    - [aircraft_location_ids](#aircraft_location_ids)
    - [aircraft_location](#aircraft_location)
    - [aircraft_power_ids](#aircraft_power_ids)
    - [aircraft_power](#aircraft_power)
    - [flight_data_ids](#flight_data_ids)
    - [flight_data](#flight_data)

## Format of the request payload and response

### Request

The **payload** that is sent to Traffic Control is a JSON formatted string. It
can be transmitted via GET or POST.

| FIELD                                      | TYPE              | REQ / OPT | INFORMATION                                |
|--------------------------------------------|-------------------|-----------|--------------------------------------------|
| drone_id \| intersection_id \| corridor_id | string            | required  | ID of the drone, intersection or corridor. |
| data_type                                  | string (constant) | required  | The value is specified for each interface. |
| data                                       | dictionary        | optional  | Additional data.                           |

<details><summary>Sample payload without data field.</summary><p>

```json
{
    "drone_id": "demo_drone",
    "data_type": "aircraft_location"
}
```

</details>

<details><summary>Sample payload with data field.</summary><p>

```json
{
    "drone_id": "demo_drone",
    "data_type": "aircraft_location",
    "data": {
        "data_id": 42
    }
}
```

</details>

### Response

The response from Traffic Control is a JSON formatted string.

| FIELD         | TYPE       | VALUE SET? | INFORMATION               |
|---------------|------------|------------|---------------------------|
| executed      | boolean    | always     | Was the command executed? |
| errors        | list       | always     |                           |
| warnings      | list       | always     |                           |
| response_data | dictionary | optional   |                           |

If one or more errors occured, they are added to the errors list.

| FIELD   | TYPE   | VALUE SET? | INFORMATION                   |
|---------|--------|------------|-------------------------------|
| err_id  | int    | always     |                               |
| err_msg | string | always     | Human readable error message. |

<details><summary>Sample error</summary><p>

```json
{
    "err_id": 1,
    "err_msg": "I am an error!"
}
```

</details>

If one or more warnings occured, they are added to the warnings list.

| FIELD    | TYPE   | VALUE SET? | INFORMATION                     |
|----------|--------|------------|---------------------------------|
| warn_id  | int    | always     |                                 |
| warn_msg | string | always     | Human readable warning message. |

<details><summary>Sample warning</summary><p>

```json
{
    "warn_id": 1,
    "warn_msg": "I am a warning!"
}
```

</details>

<details><summary>Sample response: Successful</summary><p>

```json
{
    "executed": true,
    "errors": [],
    "warnings": []
}
```

</details>

<details><summary>Sample response: Successful with one warning</summary><p>

```json
{
    "executed": true,
    "errors": [],
    "warnings": [
        {
            "warn_id": 1,
            "warn_msg": "New Traffic Control version available. Please update!"
        }
    ]
}
```

</details>

<details><summary>Sample response: Successful with response payload</summary><p>

```json
{
    "executed": true,
    "errors": [],
    "warnings": [],
    "response_data": {
        "gps_signal_level": 5,
        "gps_satellites_connected": 12,

        "gps_valid": true,
        "gps_lat": 48.26586,
        "gps_lon": 11.67436,

        "altitude": 42,

        "velocity_x": 0,
        "velocity_y": 0,
        "velocity_z": 0,

        "pitch": 0,
        "yaw": 0,
        "roll": 0
    }
}
```

</details>


## Interfaces

### intersection_list

One can request a list of intersections.

#### Request

The `data_type` is `intersection_list`.

The `intersection_id` is a search pattern like in SQL. Use `%` to match any
sequence and `_` to match any one character. You can use `!` as the escape
character.

<details><summary>Sample payload: Get all intersections</summary><p>

```json
{
    "intersection_id": "%",
    "data_type": "intersection_list"
}
```

</details>

<details><summary>Sample payload: Get all intersections starting with `campus-`</summary><p>

```json
{
    "intersection_id": "campus-%",
    "data_type": "intersection_list"
}
```

</details>

#### Response

**response_data field**

| FIELD                | TYPE | VALUE SET? | INFORMATION       |
|----------------------|------|------------|-------------------|
| &lt;intersection&gt; | dict | always     | One intersection. |

**NOTE:** The `<intersection>` dictionary has the id of the intersection as the
key. There can be none, one or multiple `<intersection>` fields in the
`response_data` field. See sample response.

<details><summary>Sample response</summary><p>

```json
{
    "executed": true,
    "errors": [],
    "warnings": [],
    "response_data": {
        "campus-int-1": {
            "id": "campus-int-1",
            "altitude": 10,
            "gps_lat": 48.047679,
            "gps_lon": 11.652243
        },
        "campus-int-2": {
            "id": "campus-int-2",
            "altitude": 15,
            "gps_lat": 48.046641,
            "gps_lon": 11.652629
        },
        "campus-int-3": {
            "id": "campus-int-3",
            "altitude": 10,
            "gps_lat": 48.0468,
            "gps_lon": 11.654028
        }
    }
}
```

</details>

### intersection_location

One can request information about the location of an intersection.

#### Request

The `data_type` is `intersection_location`.

<details><summary>Sample payload</summary><p>

```json
{
    "intersection_id": "demo_intersection",
    "data_type": "intersection_location"
}
```

</details>

#### Response

**response_data field**

| FIELD    | TYPE  | VALUE SET? | INFORMATION |
|----------|-------|------------|-------------|
| gps_lat  | float | always     | Latitude.   |
| gps_lon  | float | always     | Longitude.  |
| altitude | float | always     | In meters.  |

<details><summary>Sample response</summary><p>

```json
{
    "executed": true,
    "errors": [],
    "warnings": [],
    "response_data": {
        "gps_lat": 48.26586,
        "gps_lon": 11.67436,

        "altitude": 42
    }
}
```

</details>

### corridor_list

One can request a list of corridors.

#### Request

The `data_type` is `corridor_list`.

The `corridor_id` is a search pattern like in SQL. Use `%` to match any
sequence and `_` to match any one character. You can use `!` as the escape
character.

<details><summary>Sample payload: Get all corridors</summary><p>

```json
{
    "corridor_id": "%",
    "data_type": "corridor_list"
}
```

</details>

<details><summary>Sample payload: Get all corridors starting with `campus-`</summary><p>

```json
{
    "corridor_id": "campus-%",
    "data_type": "corridor_list"
}
```

</details>

#### Response

**response_data field**

| FIELD            | TYPE | VALUE SET? | INFORMATION   |
|------------------|------|------------|---------------|
| &lt;corridor&gt; | dict | always     | One corridor. |

**NOTE:** The `<corridor>` dictionary has the id of the corridor as the key.
There can be none, one or multiple `<corridor>` fields in the
`response_data` field. See sample response.

<details><summary>Sample response</summary><p>

```json
{
    "executed": true,
    "errors": [],
    "warnings": [],
    "response_data": {
        "campus-cor-1": {
            "id": "campus-cor-1",
            "intersection_a": "campus-int-1",
            "intersection_b": "campus-int-2"
        },
        "campus-cor-2": {
            "id": "campus-cor-2",
            "intersection_a": "campus-int-2",
            "intersection_b": "campus-int-3"
        },
        "campus-cor-3": {
            "id": "campus-cor-3",
            "intersection_a": "campus-int-3",
            "intersection_b": "campus-int-1"
        }
    }
}
```

</details>

### corridor_location

One can request information about the location of a corridor.

#### Request

The `data_type` is `corridor_location`.

<details><summary>Sample payload</summary><p>

```json
{
    "corridor_id": "demo_corridor",
    "data_type": "corridor_location"
}
```

</details>

#### Response

**response_data field**

| FIELD          | TYPE   | VALUE SET? | INFORMATION           |
|----------------|--------|------------|-----------------------|
| intersection_a | string | always     | Id of intersection A. |
| intersection_b | string | always     | Id of intersection B. |

<details><summary>Sample response</summary><p>

```json
{
    "executed": true,
    "errors": [],
    "warnings": [],
    "response_data": {
        "intersection_a": "demo_intersection_1",
        "intersection_b": "demo_intersection_2"
    }
}
```

</details>

### drone_ids

One can request a list of drone ids.

#### Request

The `data_type` is `drone_ids`.

The `dataset_id` is a search pattern like in SQL. Use `%` to match any
sequence and `_` to match any one character. You can use `!` as the escape
character.

**NOTE:** You will most likely want to to use `%` to match all ids.

<details><summary>Sample payload: Get all drone ids</summary><p>

```json
{
    "dataset_id": "%",
    "data_type": "drone_ids"
}
```

</details>

#### Response

**response_data field**

| FIELD     | TYPE     | VALUE SET? | INFORMATION            |
|-----------|----------|------------|------------------------|
| drone_ids | [string] | always     | The list of drone ids. |

<details><summary>Sample response</summary><p>

```json
{
    "executed": true,
    "errors": [],
    "warnings": [],
    "response_data": {
        "drone_ids": [
            "demo_drone",
            "other_demo_drone"
        ]
    }
}
```

</details>

### aircraft_location_ids

One can request a list of aircraft_location dataset ids.

#### Request

The `data_type` is `aircraft_location_ids`.

<details><summary>Sample payload: Get all aircraft_location dataset ids</summary><p>

```json
{
    "drone_id": "demo_drone",
    "data_type": "aircraft_location_ids"
}
```

</details>

#### Response

**response_data field**

| FIELD  | TYPE | VALUE SET? | INFORMATION                                |
|--------|------|------------|--------------------------------------------|
| min_id | int  | always     | The minimum id available. Normally 0 or 1. |
| max_id | int  | always     | The maximum id available                   |

<details><summary>Sample response</summary><p>

```json
{
    "executed": true,
    "errors": [],
    "warnings": [],
    "response_data": {
        "min_id": 1,
        "max_id": 42
    }
}
```

</details>

### aircraft_location

One can request information about the location of a drone.

#### Request

The `data_type` is `aircraft_location`.

**Payload - data field (optional)**

| FIELD   | TYPE | REQ / OPT | INFORMATION           |
|---------|------|-----------|-----------------------|
| data_id | int  | required  | ID of the data entry. |

**Note:** *data_id* must be specified when the data-field is specified.

<details><summary>Sample payload: Latest dataset</summary><p>

```json
{
    "drone_id": "demo_drone",
    "data_type": "aircraft_location"
}
```

</details>

<details><summary>Sample payload: Specific dataset</summary><p>

```json
{
    "drone_id": "demo_drone",
    "data_type": "aircraft_location",
    "data": {
        "data_id": 42
    }
}
```

</details>

#### Response

**response_data field**

| FIELD                    | TYPE    | VALUE SET? | INFORMATION                                        |
|--------------------------|---------|------------|----------------------------------------------------|
| transaction_uuid         | string  | always     | UUID of the dataset transaction in the blockchain. |
| gps_signal_level         | int     | always     | 0 (no gps signal) - 5 (very good gps signal)       |
| gps_satellites_connected | int     | always     | Number of gps-satellites connected.                |
| gps_valid                | boolean | always     | Whether the drone has a (valid) gps-signal.        |
| gps_lat                  | float   | always     | Latitude.                                          |
| gps_lon                  | float   | always     | Longitude.                                         |
| altitude                 | float   | always     | In meters.                                         |
| velocity_x               | float   | always     | Velocity X (towards north) in meters / second.     |
| velocity_y               | float   | always     | Velocity Y (towards east) in meters / second.      |
| velocity_z               | float   | always     | Velocity Z (towards down) in meters / second.      |
| pitch                    | float   | always     | [-180;180].                                        |
| yaw                      | float   | always     | [-180;180].                                        |
| roll                     | float   | always     | [-180;180].                                        |

<details><summary>Sample response</summary><p>

```json
{
    "executed": true,
    "errors": [],
    "warnings": [],
    "response_data": {
        "transaction_uuid": "00000000-0000-0000-000000000000",

        "gps_signal_level": 5,
        "gps_satellites_connected": 12,

        "gps_valid": true,
        "gps_lat": 48.26586,
        "gps_lon": 11.67436,

        "altitude": 42,

        "velocity_x": 0,
        "velocity_y": 0,
        "velocity_z": 0,

        "pitch": 0,
        "yaw": 0,
        "roll": 0
    }
}
```

</details>

### aircraft_power_ids

One can request a list of aircraft_power dataset ids.

#### Request

The `data_type` is `aircraft_power_ids`.

<details><summary>Sample payload: Get all aircraft_power dataset ids</summary><p>

```json
{
    "drone_id": "demo_drone",
    "data_type": "aircraft_power_ids"
}
```

</details>

#### Response

**response_data field**

| FIELD  | TYPE | VALUE SET? | INFORMATION                                |
|--------|------|------------|--------------------------------------------|
| min_id | int  | always     | The minimum id available. Normally 0 or 1. |
| max_id | int  | always     | The maximum id available                   |

<details><summary>Sample response</summary><p>

```json
{
    "executed": true,
    "errors": [],
    "warnings": [],
    "response_data": {
        "min_id": 1,
        "max_id": 42
    }
}
```

</details>

### aircraft_power

One can request information about the state of charge and range of a drone.

#### Request

The `data_type` is `aircraft_power`.

**Payload - data field (optional)**

| FIELD   | TYPE | REQ / OPT | INFORMATION           |
|---------|------|-----------|-----------------------|
| data_id | int  | required  | ID of the data entry. |

**Note:** *data_id* must be specified when the data-field is specified.

<details><summary>Sample payload: Latest dataset</summary><p>

```json
{
    "drone_id": "demo_drone",
    "data_type": "aircraft_power"
}
```

</details>

<details><summary>Sample payload: Specific dataset</summary><p>

```json
{
    "drone_id": "demo_drone",
    "data_type": "aircraft_power",
    "data": {
        "data_id": 42
    }
}
```

</details>

#### Response

**response_data field**

| FIELD                     | TYPE   | VALUE SET? | INFORMATION                                        |
|---------------------------|--------|------------|----------------------------------------------------|
| transaction_uuid          | string | always     | UUID of the dataset transaction in the blockchain. |
| battery_remaining         | int    | always     | In mAh.                                            |
| battery_remaining_percent | int    | always     | In %.                                              |
| remaining_flight_time     | int    | always     | In seconds.                                        |
| remaining_flight_radius   | float  | always     | In meters.                                         |

<details><summary>Sample response</summary><p>

```json
{
    "executed": true,
    "errors": [],
    "warnings": [],
    "response_data": {
        "transaction_uuid": "00000000-0000-0000-000000000000",

        "battery_remaining": 4500,
        "battery_remaining_percent": 42,

        "remaining_flight_time": 550,
        "remaining_flight_radius": 4320.5
    }
}
```

</details>

### flight_data_ids

One can request a list of flight_data dataset ids.

#### Request

The `data_type` is `flight_data_ids`.

<details><summary>Sample payload: Get all flight_data dataset ids</summary><p>

```json
{
    "drone_id": "demo_drone",
    "data_type": "flight_data_ids"
}
```

</details>

#### Response

**response_data field**

| FIELD  | TYPE | VALUE SET? | INFORMATION                                |
|--------|------|------------|--------------------------------------------|
| min_id | int  | always     | The minimum id available. Normally 0 or 1. |
| max_id | int  | always     | The maximum id available                   |

<details><summary>Sample response</summary><p>

```json
{
    "executed": true,
    "errors": [],
    "warnings": [],
    "response_data": {
        "min_id": 1,
        "max_id": 42
    }
}
```

</details>

### flight_data

One can request information about the takeoff / landing time and coordinates of
a drone.

#### Request

The `data_type` is `flight_data`.

**Payload - data field (optional)**

| FIELD   | TYPE | REQ / OPT | INFORMATION           |
|---------|------|-----------|-----------------------|
| data_id | int  | required  | ID of the data entry. |

**Note:** *data_id* must be specified when the data-field is specified.

<details><summary>Sample payload: Latest dataset</summary><p>

```json
{
    "drone_id": "demo_drone",
    "data_type": "flight_data"
}
```

</details>

<details><summary>Sample payload: Specific dataset</summary><p>

```json
{
    "drone_id": "demo_drone",
    "data_type": "flight_data",
    "data": {
        "data_id": 42
    }
}
```

</details>

#### Response

**response_data field**

| FIELD             | TYPE                    | VALUE SET? | INFORMATION                                        |
|-------------------|-------------------------|------------|----------------------------------------------------|
| transaction_uuid  | string                  | always     | UUID of the dataset transaction in the blockchain. |
| takeoff_time      | int                     | always     | UNIX timestamp.                                    |
| takeoff_gps_valid | boolean                 | always     | GPS-coordinates valid?                             |
| takeoff_gps_lat   | float                   | always     | Latitude.                                          |
| takeoff_gps_lon   | float                   | always     | Longitude.                                         |
| landing_time      | int                     | always     | UNIX timestamp.                                    |
| landing_gps_valid | boolean                 | always     | GPS-coordinates valid?                             |
| landing_gps_lat   | float                   | always     | Latitude.                                          |
| landing_gps_lon   | float                   | always     | Longitude.                                         |
| operation_modes   | [string] as json-string | always     | The last X Operation Modes.                        |

<details><summary>Sample response</summary><p>

```json
{
    "executed": true,
    "errors": [],
    "warnings": [],
    "response_data": {
        "transaction_uuid": "00000000-0000-0000-000000000000",

        "takeoff_time": 1678264333,
        "takeoff_gps_valid": "1",
        "takeoff_gps_lat": 48.26586,
        "takeoff_gps_lon": 11.67436,

        "landing_time": 1678264389,
        "landing_gps_valid": "1",
        "landing_gps_lat": 48.26586,
        "landing_gps_lon": 11.67436,
        
        "operation_modes": "[\"OnGround\", \"Landing\", \"Hovering\", \"TakeOff\", \"OnGround\"]"
    }
}
```

</details>
