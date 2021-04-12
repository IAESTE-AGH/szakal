CREATE EXTENSION pgcrypto;
CREATE TABLE users(
    user_id INT NOT NULL,
    email VARCHAR(50),
    username VARCHAR(50),
    password TEXT NOT NULL,
    name VARCHAR(25),
    surname VARCHAR(25),
    working_group VARCHAR(10),
    created_at TIMESTAMP,
    logins INT,
    last_login TIMESTAMP,
    accepted BOOLEAN,
    active BOOLEAN,
    points INT,
    PRIMARY KEY (user_id)
);

CREATE TABLE companies(
    company_id INT NOT NULL,
    name TEXT,
    address TEXT,
    phone VARCHAR(15),
    www TEXT,
    email VARCHAR(50),
    insert_date TIMESTAMP,
    update_date TIMESTAMP,
    update_user_id INT,
    deleted BOOLEAN,
    delete_date TIMESTAMP,
    rating FLOAT,
    number_of_ratings INT,
    PRIMARY KEY (company_id)
);

CREATE TABLE contact_persons(
    contact_person_id INT NOT NULL,
    company_id INT NOT NULL,
    name VARCHAR(50),
    position VARCHAR(50),
    email VARCHAR(75),
    phone VARCHAR(15),
    PRIMARY KEY (contact_person_id),
    FOREIGN KEY (company_id) REFERENCES companies (company_id)
);

CREATE TABLE events (
    event_id  INT NOT NULL,
    name    VARCHAR(20),
    PRIMARY KEY (event_id)
);

CREATE TABLE assignments (
    event_id    INT NOT NULL,
    user_id INT NOT NULL,
    company_id INT NOT NULL,
    active  BOOLEAN,
    PRIMARY KEY (event_id, user_id, company_id),
    FOREIGN KEY (event_id)  REFERENCES events (event_id),
    FOREIGN KEY (user_id)  REFERENCES users (user_id),
    FOREIGN KEY (company_id)  REFERENCES companies (company_id),
);

CREATE TABLE statuses (
    status_id INT NOT NULL,
    sort_order INT NOT NULL,
    name VARCHAR(20),
    PRIMARY KEY (status_id)
);

CREATE TABLE types (
    type_id INT NOT NULL,
    name VARCHAR(20),
    PRIMARY KEY (type_id)
);

CREATE TABLE categories (
    category_id INT NOT NULL,
    name VARCHAR(20),
    PRIMARY KEY (category_id)
);

CREATE TABLE categories_companies (
    category_id INT NOT NULL,
    company_id INT NOT NULL,
    PRIMARY KEY (category_id, company_id),
    FOREIGN KEY (category_id) REFERENCES categories (category_id),
    FOREIGN KEY (company_id) REFERENCES companies (company_id)
);

CREATE TABLE industries (
    industry_id INT NOT NULL,
    name VARCHAR(20),
    PRIMARY KEY (industry_id)
);

CREATE TABLE industries_companies (
    industry_id INT NOT NULL,
    company_id INT NOT NULL,
    PRIMARY KEY (industry_id, company_id),
    FOREIGN KEY (industry_id) REFERENCES industries (industry_id),
    FOREIGN KEY (company_id) REFERENCES companies (company_id)
);

CREATE TABLE contacts (
    contact_id INT NOT NULL,
    contact_person_id INT NOT NULL,
    type_id INT NOT NULL,
    event_id INT NOT NULL,
    status_id INT NOT NULL,
    company_id INT NOT NULL,
    user_id INT NOT NULL,
    accepted BOOLEAN,
    last_update TIMESTAMP,
    date TIMESTAMP,
    comment TEXT,
    rating INT,
    PRIMARY KEY (contact_id),
    FOREIGN KEY (contact_person_id) REFERENCES contact_persons (contact_person_id),
    FOREIGN KEY (type_id) REFERENCES types (type_id),
    FOREIGN KEY (event_id) REFERENCES events (event_id),
    FOREIGN KEY (status_id) REFERENCES statuses (status_id),
    FOREIGN KEY (company_id) REFERENCES companies (company_id),
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);