CREATE TABLE fields (
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    description VARCHAR(255),
    type VARCHAR(20) NOT NULL
);

CREATE TABLE pages (
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    description VARCHAR(255),
    fields INTEGER[] REFERENCES fields(id),
    filters INTEGER[] REFERENCES filters(id)
);

CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    description VARCHAR(255),
    rights INTEGER[] NOT NULL REFERENCES pages(id)
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(512) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    group_id INTEGER NOT NULL REFERENCES groups(id)
);

CREATE TABLE filters (
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    description VARCHAR(255),
    type VARCHAR(20) NOT NULL,
    field INTEGER NOT NULL REFERENCES fields(id)
);

CREATE TABLE objects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    description VARCHAR(255)
);

CREATE TABLE currencies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(20),
    iso_code VARCHAR(3),
    symbol VARCHAR(5) NOT NULL,
    description VARCHAR(255)
);

CREATE TABLE status (
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    description VARCHAR(255)
);

CREATE TABLE offers (
    id SERIAL PRIMARY KEY,
    user INTEGER NOT NULL REFERENCES users(id),
    description VARCHAR(255),
    object INTEGER NOT NULL REFERENCES objects(id),
    price NUMERIC(6,2) NOT NULL,
    currency INTEGER NOT NULL REFERENCES currencies(id),
    status INTEGER NOT NULL REFERENCES status(id)
);

CREATE TABLE demands (
    id SERIAL PRIMARY KEY,
    user INTEGER NOT NULL REFERENCES users(id),
    description VARCHAR(255),
    object INTEGER NOT NULL REFERENCES objects(id),
    status INTEGER NOT NULL REFERENCES status(id)
);
