-- CREATE DATABASE say_no_to_hostel;
-- if database doesn't exist


-- create table public.tenant
CREATE TABLE IF NOT EXISTS public.tenant (
    id INTEGER,
    full_name VARCHAR(100),
    sex CHAR,
    city VARCHAR(30),
    personal_qualities TEXT,
    age INTEGER,
    solvency BOOLEAN
);


-- create table public.landlord
CREATE TABLE IF NOT EXISTS public.landlord (
    id INTEGER,
    full_name VARCHAR(100),
    city VARCHAR(30),
    rating REAL,
    age INTEGER
);


-- create table public.flat
CREATE TABLE IF NOT EXISTS public.flat (
    id SERIAL,
    owner_id INTEGER,
    price INTEGER,
    square REAL,
    address VARCHAR(100),
    metro VARCHAR(30),
    floor INTEGER,
    max_floor INTEGER,
    description TEXT
);
