CREATE TABLE account
(
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE  NOT NULL,
    password VARCHAR NOT NULL,
    email    VARCHAR(50) UNIQUE NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT false
);

CREATE TABLE forum
(
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    creator_account INTEGER REFERENCES account(id),
    private BOOLEAN NOT NULL DEFAULT false,
    password VARCHAR
);


CREATE TABLE private_forum_account
(
    account_id INTEGER REFERENCES account(id) NOT NULL,
    forum_id INTEGER REFERENCES forum(id) NOT NULL
);

CREATE TABLE topic
(
    id SERIAL PRIMARY KEY,
    forum_id INTEGER REFERENCES forum(id) NOT NULL,
    account_id INTEGER REFERENCES account(id) NOT NULL,
    title VARCHAR(100),
    body TEXT NOT NULL
);

CREATE TABLE comment
(
    id SERIAL PRIMARY KEY,
    account_id INTEGER REFERENCES account(id) NOT NULL,
    topic_id INTEGER REFERENCES topic(id) NOT NULL,
    body TEXT
);

