# Documentation - API - ASK

With the ASK interfaces, one can **request information from** Traffic Control.

These interfaces are accessible via `<server_domain>/api/ask/<interface>`.

## Overview

- [Format of the request payload and response](#format-of-the-request-payload-and-response)
- [Interfaces](#interfaces)
    - [aircraft_location](#aircraft_location)
    - [aircraft_power](#aircraft_power)

## Format of the request payload and response

### Request

The **payload** that is sent to Traffic Control is a JSON formatted string. It
can be transmitted via GET or POST.

| FIELD     | TYPE              | REQ / OPT | INFORMATION                                |
|-----------|-------------------|-----------|--------------------------------------------|
| drone_id  | string            | required  | ID of the drone.                           |
| data_type | string (constant) | required  | The value is specified for each interface. |
| data      | dictionary        | optional  | Additional data.                           |

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

| FIELD                    | TYPE    | VALUE SET? | INFORMATION                                  |
|--------------------------|---------|------------|----------------------------------------------|
| gps_signal_level         | int     | always     | 0 (no gps signal) - 5 (very good gps signal) |
| gps_satellites_connected | int     | always     | Number of gps-satellites connected.          |
| gps_valid                | boolean | always     | Whether the drone has a (valid) gps-signal.  |
| gps_lat                  | float   | always     | Latitude.                                    |
| gps_lon                  | float   | always     | Longitude.                                   |
| altitude                 | float   | always     | Altitude in meters.                          |
| velocity_x               | float   | always     | Velocity X in meters / second.               |
| velocity_y               | float   | always     | Velocity Y in meters / second.               |
| velocity_z               | float   | always     | Velocity Z in meters / second.               |
| pitch                    | float   | always     | [-180;180].                                  |
| yaw                      | float   | always     | [-180;180].                                  |
| roll                     | float   | always     | [-180;180].                                  |

<details><summary>Sample response</summary><p>

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

| FIELD                     | TYPE  | VALUE SET? | INFORMATION |
|---------------------------|-------|------------|-------------|
| battery_remaining         | int   | always     | In mAh.     |
| battery_remaining_percent | int   | always     | In %.       |
| remaining_flight_time     | int   | always     | In seconds. |
| remaining_flight_radius   | float | always     | In meters.  |

<details><summary>Sample response</summary><p>

```json
{
    "executed": true,
    "errors": [],
    "warnings": [],
    "response_data": {
        "battery_remaining": 4500,
        "battery_remaining_percent": 42,
        "remaining_flight_time": 550,
        "remaining_flight_radius": 4320.5
    }
}
```

</details>
