-- CREATE DATABASE say_no_to_hostel;
-- if database doesn't exist


-- create table public.tenant
CREATE TABLE IF NOT EXISTS public.tenant (
    id BIGINT,
    full_name VARCHAR(100),
    sex CHAR,
    city VARCHAR(30),
    personal_qualities TEXT,
    age INTEGER,
    solvency BOOLEAN,
    username VARCHAR(35)
);


-- create table public.landlord
CREATE TABLE IF NOT EXISTS public.landlord (
    id BIGINT,
    full_name VARCHAR(100),
    city VARCHAR(30),
    rating REAL,
    age INTEGER,
    phone VARCHAR(15),
    username VARCHAR(35)
);


-- create table public.flat
CREATE TABLE IF NOT EXISTS public.flat (
    id SERIAL,
    owner_id BIGINT,
    price INTEGER,
    rooms INTEGER,
    square REAL,
    address VARCHAR(200),
    metro VARCHAR(30),
    floor INTEGER,
    max_floor INTEGER,
    description TEXT
);

-- create table public.flat_photo
CREATE TABLE IF NOT EXISTS public.flat_photo (
    flat_id INTEGER,
    photo VARCHAR(200)
);


-- create table public.neighborhood
CREATE TABLE IF NOT EXISTS public.neighborhood (
    id SERIAL,
    tenant_id BIGINT,
    neighbors INTEGER,
    price INTEGER,
    place TEXT,
    sex CHAR,
    preferences TEXT
);


-- create table public.goods
CREATE TABLE IF NOT EXISTS public.goods (
    id SERIAL,
    owner_id BIGINT,
    name VARCHAR(50),
    price INTEGER,
    condition CHAR,
    bargain BOOLEAN
);


-- create table public.subscription_landlord
CREATE TABLE IF NOT EXISTS public.subscription_landlord (
    tenant_id BIGINT,
    landlord_id BIGINT
);


-- create table public.likes_flats
CREATE TABLE IF NOT EXISTS public.likes_flat (
    tenant_id BIGINT,
    flat_id INTEGER
);


-- create table public.subscription_flat
CREATE TABLE IF NOT EXISTS public.subscription_flat (
    tenant_id BIGINT,
    min_price INTEGER,
    max_price INTEGER,
    min_rooms INTEGER,
    max_rooms INTEGER,
    min_square REAL,
    max_square REAL
);


-- create table public.subscription_metro
    CREATE TABLE IF NOT EXISTS public.subscription_metro (
    tenant_id BIGINT,
    metro VARCHAR(30)
);
