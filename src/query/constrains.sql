-- function that adds constraint if it doesn't exist
CREATE OR REPLACE FUNCTION public.create_constraint (t_name text, c_name text, c_sql text)
RETURNS VOID AS
$$
BEGIN
    IF NOT EXISTS (SELECT constraint_name
                   FROM information_schema.constraint_column_usage
                   WHERE table_name = t_name AND constraint_name = c_name) then
        execute c_sql;
    END IF;
END;
$$
LANGUAGE 'plpgsql';


-- create constraints to public.tenant
SELECT public.create_constraint (
    'tenant',
    'tenant_pkey',
    'ALTER TABLE public.tenant ADD CONSTRAINT tenant_pkey PRIMARY KEY (id);'
);

SELECT public.create_constraint (
    'tenant',
    'tenant_id_check',
    'ALTER TABLE public.tenant ADD CONSTRAINT tenant_id_check CHECK (id > 0 AND id IS NOT NULL);'
);

SELECT public.create_constraint(
    'tenant',
    'tenant_full_name_check',
    'ALTER TABLE public.tenant ADD CONSTRAINT tenant_full_name_check CHECK (full_name IS NOT NULL);'
);

SELECT public.create_constraint(
    'tenant',
    'tenant_sex_check',
    'ALTER TABLE public.tenant ADD CONSTRAINT tenant_sex_check CHECK (sex IN (''M'', ''F'') AND sex IS NOT NULL);'
);

SELECT public.create_constraint(
    'tenant',
    'tenant_city_check',
    'ALTER TABLE public.tenant ADD CONSTRAINT tenant_city_check CHECK (city IS NOT NULL);'
);

SELECT public.create_constraint(
    'tenant',
    'tenant_age_check',
    'ALTER TABLE public.tenant ADD CONSTRAINT tenant_age_check CHECK (age >= 14 AND age <= 100 AND age IS NOT NULL);'
);


-- create constraints to public.landlord
SELECT public.create_constraint(
    'landlord',
    'landlord_pkey',
    'ALTER TABLE public.landlord ADD CONSTRAINT landlord_pkey PRIMARY KEY (id);'
);

SELECT public.create_constraint (
    'landlord',
    'landlord_id_check',
    'ALTER TABLE public.landlord ADD CONSTRAINT landlord_id_check CHECK (id > 0 AND id IS NOT NULL);'
);

SELECT public.create_constraint(
    'landlord',
    'landlord_full_name_check',
    'ALTER TABLE public.landlord ADD CONSTRAINT landlord_full_name_check CHECK (full_name IS NOT NULL);'
);

SELECT public.create_constraint(
    'landlord',
    'landlord_city_check',
    'ALTER TABLE public.landlord ADD CONSTRAINT landlord_city_check CHECK (city IS NOT NULL);'
);

SELECT public.create_constraint(
    'landlord',
    'landlord_rating_check',
    'ALTER TABLE public.landlord ADD CONSTRAINT landlord_rating_check CHECK (rating >= 0.0 AND rating <= 10.0 AND rating IS NOT NULL);'
);

SELECT public.create_constraint(
    'landlord',
    'landlord_age_check',
    'ALTER TABLE public.landlord ADD CONSTRAINT landlord_age_check CHECK (age >= 14 AND age <= 100 AND age IS NOT NULL);'
);