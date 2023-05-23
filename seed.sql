-- Drop the database if it exists
DROP DATABASE IF EXISTS sky_time;

-- Create the database
CREATE DATABASE sky_time;

-- Connect to the database
\c sky_time;

-- Create the necessary tables

-- Table: users
CREATE TABLE users (
    username VARCHAR(50) PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    image_url TEXT DEFAULT '/static/images/default_img.png',
    password TEXT NOT NULL
);

-- Table: locations
CREATE TABLE locations (
    location_id SERIAL PRIMARY KEY,
    username VARCHAR(50) REFERENCES users(username),
    latitude FLOAT,
    longitude FLOAT,
    city VARCHAR(100),
    country VARCHAR(100),
    date DATE
);

-- Table: users_favourites
CREATE TABLE users_favourites (
    favourite_id SERIAL PRIMARY KEY,
    location_id INTEGER REFERENCES locations(location_id),
    date DATE,
    sunrise_time TIME,
    sunset_time TIME,
    moonrise_time TIME,
    moonset_time TIME,
    day_length TIME
);
