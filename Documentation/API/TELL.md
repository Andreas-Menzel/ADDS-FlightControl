# Documentation - API - ASK

With the TELL interfaces, one can **send information to** Traffic Control.

These interfaces are accessible via `<server_domain>/api/tell/<interface>`.

## Overview

- [Format of the request payload and response](#format-of-the-request-payload-and-response)
- [Interfaces](#interfaces)
    - [intersection_location](#intersection_location)
    - [delete_intersection](#delete_intersection)
    - [corridor_location](#corridor_location)
    - [delete_corridor](#delete_corridor)
    - [aircraft_location](#aircraft_location)
    - [aircraft_power](#aircraft_power)
    - [flight_data](#flight_data)
    - [register_drone](#register_drone)

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
    "data_type": "register_drone"
}
```

</details>

<details><summary>Sample payload with data field.</summary><p>

```json
{
    "drone_id": "demo_drone",
    "data_type": "aircraft_power",
    "data": {
        "battery_remaining": 4500,
        "battery_remaining_percent": 42,
        "remaining_flight_time": 550,
        "remaining_flight_radius": 4320.5
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


## Interfaces

### intersection_location

One can send information about the location of an intersection. The intersection
will be updated if it already exists; otherwise it will be created.

#### Request

The `data_type` is `intersection_location`.

**Payload - data field (required)**

| FIELD    | TYPE  | REQ / OPT | INFORMATION         |
|----------|-------|-----------|---------------------|
| gps_lat  | float | required  | Latitude.           |
| gps_lon  | float | required  | Longitude.          |
| altitude | float | required  | Altitude in meters. |

<details><summary>Sample payload</summary><p>

```json
{
    "intersection_id": "demo_intersection",
    "data_type": "intersection_location",
    "data": {
        "gps_lat": 48.26586,
        "gps_lon": 11.67436,

        "altitude": 42
    }
}
```

</details>

#### Response

Standard response. The `response_data` field is never set.

### delete_intersection

One can delete an intersection. This endpoint is idempotent; trying to delete an
intersection that does not exist will not result in an error.

**Note:** Make sure that the intersection is not a part of any corridor.
Otherwise the intersection will not be deleted and an error will be returned.

#### Request

The `data_type` is `delete_intersection`.

<details><summary>Sample payload: Delete intersection with id demo_intersection</summary><p>

```json
{
    "intersection_id": "demo_intersection",
    "data_type": "delete_intersection"
}
```

</details>

#### Response

Standard response. The `response_data` field is never set.

### corridor_location

One can send information about the location of a flight corridor. The corridor
will be updated if it already exists; otherwise it will be created.

#### Request

The `data_type` is `corridor_location`.

**Payload - data field (required)**

| FIELD          | TYPE   | REQ / OPT | INFORMATION         |
|----------------|--------|-----------|---------------------|
| intersection_a | string | required  | First intersection. |
| intersection_b | string | required  | Second intersection |

**NOTE:** Make sure that the intersections a and b exist before adding them to a
corridor.

<details><summary>Sample payload</summary><p>

```json
{
    "intersection_id": "demo_corridor",
    "data_type": "corridor_location",
    "data": {
        "intersection_a": "demo_intersection_1",
        "intersection_b": "demo_intersection_2"
    }
}
```

</details>

#### Response

Standard response. The `response_data` field is never set.

### delete_corridor

One can delete a corridor. This endpoint is idempotent; trying to delete a
corridor that does not exist will not result in an error.

#### Request

The `data_type` is `delete_corridor`.

<details><summary>Sample payload: Delete corridor with id demo_corridor</summary><p>

```json
{
    "corridor_id": "demo_corridor",
    "data_type": "delete_corridor"
}
```

</details>

#### Response

Standard response. The `response_data` field is never set.

### aircraft_location

One can send information about the location of a drone.

#### Request

The `data_type` is `aircraft_location`.

**Payload - data field (required)**

| FIELD                    | TYPE    | REQ / OPT | INFORMATION                                            |
|--------------------------|---------|-----------|--------------------------------------------------------|
| time_sent                | float   | required  | UNIX timestamp when the dataset was sent from the app. |
| time_recorded            | float   | required  | UNIX timestamp when the dataset was recorded.          |
| gps_signal_level         | int     | required  | 0 (no gps signal) - 5 (very good gps signal)           |
| gps_satellites_connected | int     | required  | Number of gps-satellites connected.                    |
| gps_valid                | boolean | required  | Whether the drone has a (valid) gps-signal.            |
| gps_lat                  | float   | required  | Latitude.                                              |
| gps_lon                  | float   | required  | Longitude.                                             |
| altitude                 | float   | required  | Altitude in meters.                                    |
| velocity_x               | float   | required  | Velocity X in meters / second.                         |
| velocity_y               | float   | required  | Velocity Y in meters / second.                         |
| velocity_z               | float   | required  | Velocity Z in meters / second.                         |
| pitch                    | float   | required  | [-180;180].                                            |
| yaw                      | float   | required  | [-180;180].                                            |
| roll                     | float   | required  | [-180;180].                                            |

<details><summary>Sample payload</summary><p>

```json
{
    "drone_id": "demo_drone",
    "data_type": "aircraft_location",
    "data": {
        "time_sent": 1673338740.1,
        "time_recorded": 1673338740.0,

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

#### Response

**response_data field**

| FIELD            | TYPE   | VALUE SET? | INFORMATION                                        |
|------------------|--------|------------|----------------------------------------------------|
| transaction_uuid | string | always     | UUID of the dataset transaction in the blockchain. |

<details><summary>Sample response</summary><p>

```json
{
    "executed": true,
    "errors": [],
    "warnings": [],
    "response_data": {
        "transaction_uuid": "00000000-0000-0000-000000000000",
    }
}
```

</details>

### aircraft_power

One can send information about the state of charge and range of a drone.

#### Request

The `data_type` is `aircraft_power`.

**Payload - data field (required)**

| FIELD                     | TYPE  | REQ / OPT | INFORMATION                                            |
|---------------------------|-------|-----------|--------------------------------------------------------|
| time_sent                 | float | required  | UNIX timestamp when the dataset was sent from the app. |
| time_recorded             | float | required  | UNIX timestamp when the dataset was recorded.          |
| battery_remaining         | int   | required  | In mAh.                                                |
| battery_remaining_percent | int   | required  | In %.                                                  |
| remaining_flight_time     | int   | required  | In seconds.                                            |
| remaining_flight_radius   | float | required  | In meters.                                             |

<details><summary>Sample payload</summary><p>

```json
{
    "drone_id": "demo_drone",
    "data_type": "aircraft_power",
    "data": {
        "time_sent": 1673338740.1,
        "time_recorded": 1673338740.0,

        "battery_remaining": 4500,
        "battery_remaining_percent": 42,
        
        "remaining_flight_time": 550,
        "remaining_flight_radius": 4320.5
    }
}
```

</details>

#### Response

**response_data field**

| FIELD            | TYPE   | VALUE SET? | INFORMATION                                        |
|------------------|--------|------------|----------------------------------------------------|
| transaction_uuid | string | always     | UUID of the dataset transaction in the blockchain. |

<details><summary>Sample response</summary><p>

```json
{
    "executed": true,
    "errors": [],
    "warnings": [],
    "response_data": {
        "transaction_uuid": "00000000-0000-0000-000000000000",
    }
}
```

</details>

### flight_data

One can send information about the takeoff / landing time and coordinates of a
drone.

#### Request

The `data_type` is `flight_data`.

**Payload - data field (required)**

| FIELD             | TYPE     | REQ / OPT | INFORMATION                                            |
|-------------------|----------|-----------|--------------------------------------------------------|
| time_sent         | float    | required  | UNIX timestamp when the dataset was sent from the app. |
| time_recorded     | float    | required  | UNIX timestamp when the dataset was recorded.          |
| takeoff_time      | int      | required  | UNIX timestamp.                                        |
| takeoff_gps_valid | boolean  | required  | GPS-coordinates valid?                                 |
| takeoff_gps_lat   | float    | required  | Latitude.                                              |
| takeoff_gps_lon   | float    | required  | Longitude.                                             |
| landing_time      | int      | required  | UNIX timestamp.                                        |
| landing_gps_valid | boolean  | required  | GPS-coordinates valid?                                 |
| landing_gps_lat   | float    | required  | Latitude.                                              |
| landing_gps_lon   | float    | required  | Longitude.                                             |
| operation_modes   | [string] | required  | The last X Operation Modes.                            |

<details><summary>Sample payload</summary><p>

```json
{
	"drone_id": "demo_drone",
	"data_type": "flight_data",
	"data": {
        "time_sent": 1673338740.1,
        "time_recorded": 1673338740.0,

		"takeoff_time": 1678264333,
		"takeoff_gps_valid": "true",
		"takeoff_gps_lat": 48.26586,
		"takeoff_gps_lon": 11.67436,

		"landing_time": 1678264389,
		"landing_gps_valid": "true",
		"landing_gps_lat": 48.26586,
		"landing_gps_lon": 11.67436,

		"operation_modes": ["OnGround", "Landing", "Hovering", "TakeOff", "OnGround"]
	}
}
```

</details>

#### Response

**response_data field**

| FIELD            | TYPE   | VALUE SET? | INFORMATION                                        |
|------------------|--------|------------|----------------------------------------------------|
| transaction_uuid | string | always     | UUID of the dataset transaction in the blockchain. |

<details><summary>Sample response</summary><p>

```json
{
    "executed": true,
    "errors": [],
    "warnings": [],
    "response_data": {
        "transaction_uuid": "00000000-0000-0000-000000000000",
    }
}
```

</details>

### register_drone

Before a drone can be used, it has to be registered.

#### Request

The `data_type` is `register_drone`.

**Payload - data field (required)**

**TODO:**

| FIELD    | TYPE   | REQ / OPT | INFORMATION              |
|----------|--------|-----------|--------------------------|
| crypt_id | string | required  | The Crypt-ID of the app. |

<details><summary>Sample payload</summary><p>

```json
{
	"drone_id": "demo_drone",
	"data_type": "register_drone",
	"data": {

	}
}
```

</details>

**Note:**
- The drone registration is idempotent; registering a drone a second time has no
  effect.
- If the registration could not be finished completely (e.g. the chains could
  not be created), the `execution` field is set to `false` and an appropriate
  error is set.
- If the registration did not succeed, one has to send the registration request
  again. A warning will now be set, indicating that this is not a completely new
  registration.

#### Response

Standard response. The `response_data` field is never set.
