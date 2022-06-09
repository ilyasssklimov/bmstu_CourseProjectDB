CREATE OR REPLACE FUNCTION public.create_role (r_name text, r_sql text)
RETURNS VOID AS
$$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles
                   WHERE  rolname = r_name) THEN
        EXECUTE r_sql;
    END IF;
END;
$$
LANGUAGE 'plpgsql';


DROP ROLE creator;
SELECT public.create_role(
    'creator',
    'CREATE ROLE creator LOGIN PASSWORD ''creator'';'
);
