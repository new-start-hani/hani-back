CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    hobby VARCHAR(255) NOT NULL,
    nickname VARCHAR(255) NOT NULL,
    gender VARCHAR(255) NOT NULL,
    age INTEGER NOT NULL,
    profile_image VARCHAR(255),
    disabled BOOLEAN NOT NULL
);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    category VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    user_id INTEGER REFERENCES users(id) NOT NULL
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    content VARCHAR(255) NOT NULL,
    post_id INTEGER REFERENCES posts(id) NOT NULL
);