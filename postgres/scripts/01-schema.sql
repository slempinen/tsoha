CREATE TABLE account
(
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE  NOT NULL,
    password VARCHAR NOT NULL,
    email    VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE forum
(
    id SERIAL PRIMARY KEY,
    name VARCHAR(30) UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE private_forum
(
    id SERIAL PRIMARY KEY,
    forum_id SERIAL REFERENCES forum(id) NOT NULL,
    password VARCHAR(50) NOT NULL
);

CREATE TABLE private_forum_account
(
    account_id SERIAL REFERENCES account(id) NOT NULL,
    forum_id SERIAL REFERENCES private_forum(id) NOT NULL
);

CREATE TABLE topic
(
    id SERIAL PRIMARY KEY,
    forum_id SERIAL REFERENCES forum(id) NOT NULL,
    account_id SERIAL REFERENCES account(id) NOT NULL,
    title VARCHAR(30),
    body TEXT NOT NULL
);

CREATE TABLE comment
(
    id SERIAL PRIMARY KEY,
    account_id SERIAL REFERENCES account(id) NOT NULL,
    topic_id SERIAL REFERENCES topic(id) NOT NULL,
    body TEXT
);

