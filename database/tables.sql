/*  PROJECT NAME:   b3_dm_assg
 *  FILE NAME:      tables.sql
 *
 *  2024 Keitaro Kamo (@nekoyade)
 *
 */

PRAGMA foreign_keys = true;


/* Tables */

DROP TABLE persons;
DROP TABLE phones;
DROP TABLE emails;
DROP TABLE roles;
DROP TABLE instruments;
DROP TABLE groups;
DROP TABLE venues;
DROP TABLE sections;
DROP TABLE performances;
DROP TABLE reservations;

CREATE TABLE persons (
    id VARCHAR PRIMARY KEY,
    name VARCHAR,
    birth_date VARCHAR,
    address VARCHAR
);

CREATE TABLE phones (
    person_id VARCHAR,
    phone VARCHAR,
    PRIMARY KEY (person_id, phone),
    FOREIGN KEY (person_id) REFERENCES persons (id)
);

CREATE TABLE emails (
    person_id VARCHAR,
    email VARCHAR,
    PRIMARY KEY (person_id, email),
    FOREIGN KEY (person_id) REFERENCES persons (id)
);

CREATE TABLE roles (
    person_id VARCHAR,
    role VARCHAR,
    PRIMARY KEY (person_id, role),
    FOREIGN KEY (person_id) REFERENCES persons (id)
);

CREATE TABLE instruments (
    person_id VARCHAR,
    instrument VARCHAR,
    PRIMARY KEY (person_id, instrument),
    FOREIGN KEY (person_id) REFERENCES persons (id)
);

CREATE TABLE groups (
    id VARCHAR PRIMARY KEY,
    name VARCHAR,
    address VARCHAR,
    email VARCHAR,
    type VARCHAR,
    sponsor VARCHAR,
    represented_by VARCHAR,
    FOREIGN KEY (represented_by) REFERENCES persons (id)
);

CREATE TABLE venues (
    id VARCHAR PRIMARY KEY,
    name VARCHAR,
    address VARCHAR
);

CREATE TABLE sections (
    id VARCHAR PRIMARY KEY,
    name VARCHAR,
    capacity INTEGER,
    venue_id VARCHAR,
    FOREIGN KEY (venue_id) REFERENCES venues (id)
);

CREATE TABLE performances (
    id VARCHAR,
    date VARCHAR,
    time_slot VARCHAR,
    group_id VARCHAR,
    section_id VARCHAR,
    PRIMARY KEY (id, date, time_slot, group_id, section_id),
    FOREIGN KEY (group_id) REFERENCES groups (id),
    FOREIGN KEY (section_id) REFERENCES sections (id)
);

CREATE TABLE reservations (
    reserved_by VARCHAR,
    performance_id VARCHAR,
    date VARCHAR,
    time VARCHAR,
    PRIMARY KEY (reserved_by, performance_id),
    FOREIGN KEY (reserved_by) REFERENCES persons (id),
    FOREIGN KEY (performance_id) REFERENCES performances (id)
);


/* Join tables */

DROP TABLE households;
DROP TABLE persons_groups;

CREATE TABLE households (
    parent_id VARCHAR,
    child_id VARCHAR,
    PRIMARY KEY (parent_id, child_id),
    FOREIGN KEY (parent_id) REFERENCES persons (id),
    FOREIGN KEY (child_id) REFERENCES persons (id)
);

CREATE TABLE persons_groups (
    person_id VARCHAR,
    group_id VARCHAR,
    PRIMARY KEY (person_id, group_id),
    FOREIGN KEY (person_id) REFERENCES persons (id),
    FOREIGN KEY (group_id) REFERENCES groups (id)
);
