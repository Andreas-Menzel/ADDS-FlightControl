DROP TABLE IF EXISTS drones;
DROP TABLE IF EXISTS aircraft_location;
DROP TABLE IF EXISTS intersections;
DROP TABLE IF EXISTS corridors;

CREATE TABLE drones (
    id                          TEXT    PRIMARY KEY,
    active                      INTEGER NOT NULL    DEFAULT 0,
    
    health                      TEXT,
    battery_remaining           INTEGER,
    battery_remaining_percent   INTEGER,
    remaining_flight_time       INTEGER,
    remaining_flight_radius     FLOAT
);

CREATE TABLE aircraft_location (
    id                          INTEGER PRIMARY KEY AUTOINCREMENT,
    drone_id                    TEXT,
    
    gps_signal_level            INTEGER,
    gps_satellites_connected    INTEGER,

    gps_valid                   TEXT,
    gps_lat                     FLOAT,
    gps_lon                     FLOAT,
    altitude                    INTEGER,
    velocity_x                  FLOAT,
    velocity_y                  FLOAT,
    velocity_z                  FLOAT,
    pitch                       FLOAT,
    yaw                         FLOAT,
    roll                        FLOAT
);

CREATE TABLE intersections (
    id              TEXT    PRIMARY KEY,
    gps_lat         TEXT    NOT NULL,
    gps_lon         TEXT    NOT NULL,
    height          INT     NOT NULL
);

CREATE TABLE corridors (
    id              TEXT    PRIMARY KEY,
    intersection_a  TEXT    NOT NULL,
    intersection_b  TEXT    NOT NULL
);

INSERT INTO drones(id, active) VALUES("demo_drone", 0);

INSERT INTO intersections VALUES("EDMR-Landeplatz", "48.048121", "11.653678", 0);
INSERT INTO intersections VALUES("int_1", "48.047705", "11.653841", 0);
INSERT INTO intersections VALUES("int_2", "48.047679", "11.652243", 0);
INSERT INTO intersections VALUES("int_3", "48.046641", "11.652629", 0);
INSERT INTO intersections VALUES("int_4", "48.046800", "11.654028", 0);
INSERT INTO intersections VALUES("int_5", "48.046876", "11.655620", 0);
INSERT INTO intersections VALUES("int_6", "48.046928", "11.657085", 0);
INSERT INTO intersections VALUES("int_7", "48.047849", "11.656265", 0);

INSERT INTO corridors VALUES("cor_1", "EDMR-Landeplatz", "int_1");
INSERT INTO corridors VALUES("cor_2", "int_1", "int_2");
INSERT INTO corridors VALUES("cor_3", "int_2", "int_3");
INSERT INTO corridors VALUES("cor_4", "int_3", "int_4");
INSERT INTO corridors VALUES("cor_5", "int_4", "int_1");
INSERT INTO corridors VALUES("cor_6", "int_4", "int_5");
INSERT INTO corridors VALUES("cor_7", "int_5", "int_6");
INSERT INTO corridors VALUES("cor_8", "int_6", "int_7");
INSERT INTO corridors VALUES("cor_9", "int_5", "int_7");
INSERT INTO corridors VALUES("cor_10", "int_1", "int_7");
INSERT INTO corridors VALUES("cor_11", "int_1", "int_5");
INSERT INTO corridors VALUES("cor_12", "int_4", "int_7");