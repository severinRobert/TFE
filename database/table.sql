CREATE TABLE selections_group (
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    description VARCHAR(255)
);

CREATE TABLE selections (
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    description VARCHAR(255),
    selections_group_id INT NOT NULL,
    FOREIGN KEY (selections_group_id) REFERENCES selections_group(id)
);

CREATE TABLE fields (
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    description VARCHAR(255),
    type_id INT NOT NULL,
    is_required BOOLEAN NOT NULL,
    is_filterable BOOLEAN NOT NULL,
    selections_group_id INT,
    FOREIGN KEY (type_id) REFERENCES type(id),
    FOREIGN KEY (selections_group_id) REFERENCES selections_group(id)
);

CREATE TABLE type (
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    description VARCHAR(255)
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    description VARCHAR(255)
);

CREATE TABLE product_field (
    product_id INT NOT NULL,
    field_id INT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (field_id) REFERENCES fields(id)
);

CREATE TABLE status (
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    description VARCHAR(255)
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    email VARCHAR(20) NOT NULL,
    description VARCHAR(255)
);

CREATE TABLE offers (
    id SERIAL PRIMARY KEY,
    owner_id INT NOT NULL,
    product_id INT NOT NULL,
    status_id INT NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (status_id) REFERENCES status(id)
);

CREATE TABLE values (
    id SERIAL PRIMARY KEY,
    value VARCHAR(20) NOT NULL,
    offer_id INT NOT NULL,
    field_id INT NOT NULL,
    FOREIGN KEY (offer_id) REFERENCES offers(id),
    FOREIGN KEY (field_id) REFERENCES fields(id)
);
