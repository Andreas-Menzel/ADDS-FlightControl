DROP TABLE IF EXISTS drones;
DROP TABLE IF EXISTS aircraft_location;
DROP TABLE IF EXISTS aircraft_power;
DROP TABLE IF EXISTS flight_data;

DROP TABLE IF EXISTS intersections;
DROP TABLE IF EXISTS corridors;

DROP TABLE IF EXISTS locked_intersections;
DROP TABLE IF EXISTS locked_corridors;


CREATE TABLE drones (
    id                          TEXT    PRIMARY KEY,
    
    chain_uuid_mission          TEXT,
    chain_uuid_blackbox         TEXT
);

CREATE TABLE aircraft_location (
    id                          INTEGER AUTO INCREMENT,
    drone_id                    TEXT NOT NULL,
    time_sent                   FLOAT,
    time_recorded               FLOAT,

    transaction_uuid            TEXT,
    
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
    roll                        FLOAT,

    PRIMARY KEY (id, drone_id)
);

CREATE TRIGGER aircraft_location_increment_id
AFTER INSERT ON aircraft_location
BEGIN
    UPDATE aircraft_location
    SET id=(SELECT COALESCE(MAX(id), 0) + 1 FROM aircraft_location WHERE drone_id = NEW.drone_id)
    WHERE id IS null AND drone_id = NEW.drone_id;
END;


CREATE TABLE aircraft_power (
    id                          INTEGER AUTO INCREMENT,
    drone_id                    TEXT NOT NULL,
    time_sent                   FLOAT,
    time_recorded               FLOAT,

    transaction_uuid            TEXT,

    battery_remaining           INTEGER,
    battery_remaining_percent   INTEGER,

    remaining_flight_time       INTEGER,
    remaining_flight_radius     FLOAT,

    PRIMARY KEY (id, drone_id)
);

CREATE TRIGGER aircraft_power_increment_id
AFTER INSERT ON aircraft_power
BEGIN
  UPDATE aircraft_power
  SET id=(SELECT COALESCE(MAX(id), 0) + 1 FROM aircraft_power WHERE drone_id = NEW.drone_id)
  WHERE id IS null AND drone_id = NEW.drone_id;
END;

CREATE TABLE flight_data (
    id                          INTEGER AUTO INCREMENT,
    drone_id                    TEXT NOT NULL,
    time_sent                   FLOAT,
    time_recorded               FLOAT,

    transaction_uuid            TEXT,

    takeoff_time                INTEGER,
    takeoff_gps_valid           TEXT,
    takeoff_gps_lat             FLOAT,
    takeoff_gps_lon             FLOAT,

    landing_time                INTEGER,
    landing_gps_valid           TEXT,
    landing_gps_lat             FLOAT,
    landing_gps_lon             FLOAT,

    operation_modes             TEXT,

    PRIMARY KEY (id, drone_id)
);

CREATE TRIGGER flight_data_increment_id
AFTER INSERT ON flight_data
BEGIN
    UPDATE flight_data
    SET id=(SELECT COALESCE(MAX(id), 0) + 1 FROM flight_data WHERE drone_id = NEW.drone_id)
    WHERE id IS null AND drone_id = NEW.drone_id;
END;

CREATE TABLE mission_data (
    id                          INTEGER AUTO INCREMENT,
    drone_id                    TEXT NOT NULL,

    time_sent                   FLOAT,
    time_recorded               FLOAT,

    transaction_uuid            TEXT,

    start_intersection          TEXT,
    last_uploaded_intersection  TEXT,

    last_mission_intersection   TEXT,

    land_after_mission_finished TEXT,
    corridors_pending           TEXT,
    corridors_approved          TEXT,
    corridors_uploaded          TEXT,
    corridors_finished          TEXT,

    PRIMARY KEY (id, drone_id)
);

CREATE TRIGGER mission_data_increment_id
AFTER INSERT ON mission_data
BEGIN
    UPDATE mission_data
    SET id=(SELECT COALESCE(MAX(id), 0) + 1 FROM mission_data WHERE drone_id = NEW.drone_id)
    WHERE id IS null AND drone_id = NEW.drone_id;
END;


CREATE TABLE intersections (
    id              TEXT    PRIMARY KEY,

    gps_lat         FLOAT   NOT NULL,
    gps_lon         FLOAT   NOT NULL,

    altitude        INT     NOT NULL
);

CREATE TABLE corridors (
    id              TEXT    PRIMARY KEY,
    
    intersection_a  TEXT    NOT NULL,
    intersection_b  TEXT    NOT NULL
);


CREATE TABLE locked_intersections (
    intersection_id     TEXT    PRIMARY KEY,
    drone_id            TEXT    NOT NULL
);

CREATE TABLE locked_corridors (
    corridor_id     TEXT    PRIMARY KEY,
    drone_id        TEXT    NOT NULL
);



INSERT INTO drones (
    id, chain_uuid_mission, chain_uuid_blackbox
)
VALUES (
    "setup_drone",
    "48a5c885-43f2-4476-ba62-4340de24a472",
    "d069307f-7aa7-4efa-8845-92e464665492"
);

INSERT INTO drones (
    id, chain_uuid_mission, chain_uuid_blackbox
)
VALUES (
    "demo_drone",
    "2a536579-9ef7-4f63-aff9-c25a92a0c803",
    "1ce103f8-0e9a-4a71-9081-6a69bbc842cf"
);


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

