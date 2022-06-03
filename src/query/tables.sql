CREATE TABLE IF NOT EXISTS say_no_to_hostel.public.tenant (
    id serial,
    full_name VARCHAR(100),
    sex CHAR,
    city VARCHAR(30),
    personal_qualities TEXT,
    age INTEGER,
    solvency BOOLEAN
)