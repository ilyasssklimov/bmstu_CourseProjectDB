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

-- delete role if it exists
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


-- create guest role
SELECT public.delete_role('guest');
SELECT public.create_role('guest','CREATE ROLE guest LOGIN PASSWORD ''guest'';');
GRANT SELECT, INSERT ON public.tenant TO guest;
GRANT SELECT, INSERT ON public.landlord TO guest;
GRANT SELECT ON public.flat TO guest;
GRANT SELECT ON public.flat_photo TO guest;

-- create tenant role
SELECT public.delete_role('tenant');
SELECT public.create_role('tenant','CREATE ROLE tenant LOGIN PASSWORD ''tenant'';');
GRANT SELECT ON public.tenant TO tenant;
GRANT SELECT, UPDATE ON public.landlord TO tenant;
GRANT SELECT ON public.flat TO tenant;
GRANT SELECT ON public.flat_photo TO tenant;
GRANT INSERT, SELECT ON public.subscription_landlord TO tenant;
GRANT INSERT, SELECT ON public.likes_flat TO tenant;

-- create landlord role
SELECT public.delete_role('landlord');
SELECT public.create_role('landlord','CREATE ROLE landlord LOGIN PASSWORD ''landlord'';');
GRANT SELECT ON public.tenant TO landlord;
GRANT SELECT ON public.landlord TO landlord;
GRANT INSERT, SELECT ON public.flat TO landlord;
GRANT USAGE, SELECT ON SEQUENCE flat_id_seq TO landlord;
GRANT INSERT, SELECT ON public.flat_photo TO landlord;

-- create admin role
SELECT public.delete_role('admin');
SELECT public.create_role('admin','CREATE ROLE admin LOGIN PASSWORD ''admin'';');
GRANT postgres TO admin;