-- execute 'CREATE DATABASE say_no_to_hostel;' if database doesn't exist

-- create table public.tenant
CREATE TABLE IF NOT EXISTS public.tenant (
    id integer,
    full_name VARCHAR(100),
    sex CHAR,
    city VARCHAR(30),
    personal_qualities TEXT,
    age INTEGER,
    solvency BOOLEAN
);


-- create table public.landlord
CREATE TABLE IF NOT EXISTS public.landlord (
    id integer,
    full_name VARCHAR(100),
    city VARCHAR(30),
    rating REAL,
    age INTEGER
);