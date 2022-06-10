-- create role if it doesn't exist
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

-- delete role if if exists
CREATE OR REPLACE FUNCTION public.delete_role (r_name text)
RETURNS VOID AS
$$
BEGIN
    IF EXISTS (SELECT FROM pg_catalog.pg_roles
               WHERE  rolname = r_name) THEN
        EXECUTE FORMAT('REASSIGN OWNED BY %s TO postgres;' ||
                       'DROP OWNED BY %s;' ||
                       'DROP ROLE %s;', r_name, r_name, r_name);
    END IF;
END;
$$
LANGUAGE 'plpgsql';


-- create admin role
SELECT public.delete_role('admin');
SELECT public.create_role('admin','CREATE ROLE admin LOGIN PASSWORD ''admin'';');
GRANT postgres TO admin;

-- create guest role
SELECT public.delete_role('guest');
SELECT public.create_role('guest','CREATE ROLE guest LOGIN PASSWORD ''guest'';');
GRANT SELECT ON public.tenant TO guest;
GRANT SELECT ON public.landlord TO guest;
GRANT INSERT ON public.tenant TO guest;
GRANT INSERT ON public.landlord TO guest;
