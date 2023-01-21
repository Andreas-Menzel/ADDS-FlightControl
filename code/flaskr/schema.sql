DROP TABLE IF EXISTS drones;
DROP TABLE IF EXISTS intersections;
DROP TABLE IF EXISTS corridors;

CREATE TABLE drones (
    id              TEXT    PRIMARY KEY,
    coordinates_lat TEXT,
    coordinates_lon TEXT,
    height          INTEGER,
    heading         INTEGER,
    air_speed       INTEGER,
    ground_speed    INTEGER,
    vertical_speed  INTEGER,
    health          TEXT,
    battery_soc     INTEGER,
    rem_flight_time INTEGER
);

CREATE TABLE intersections (
    id              TEXT    PRIMARY KEY,
    coordinates_lat TEXT    NOT NULL,
    coordinates_lon TEXT    NOT NULL,
    height          INT     NOT NULL
);

CREATE TABLE corridors (
    id              TEXT    PRIMARY KEY,
    intersection_a  TEXT    NOT NULL,
    intersection_b  TEXT    NOT NULL
);
