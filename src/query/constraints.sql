-- function that adds constraint if it doesn't exist
CREATE OR REPLACE FUNCTION public.create_constraint (t_name text, c_name text, c_sql text)
RETURNS VOID AS
$$
BEGIN
    IF NOT EXISTS (SELECT constraint_name
                   FROM information_schema.constraint_column_usage
                   WHERE table_name = t_name AND constraint_name = c_name) THEN
        EXECUTE c_sql;
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

SELECT public.create_constraint(
    'landlord',
    'landlord_phone_check',
    'ALTER TABLE public.landlord ADD CONSTRAINT landlord_phone_check CHECK (char_length(phone) > 10 AND phone IS NOT NULL);'
);


-- create constraints to public.flat
SELECT public.create_constraint(
    'flat',
    'flat_pkey',
    'ALTER TABLE public.flat ADD CONSTRAINT flat_pkey PRIMARY KEY (id);'
);

SELECT public.create_constraint (
    'landlord',
    'flat_owner_id_fkey',
    'ALTER TABLE public.flat ADD CONSTRAINT flat_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public.landlord (id);'
);

SELECT public.create_constraint (
    'flat',
    'flat_owner_id_check',
    'ALTER TABLE public.flat ADD CONSTRAINT flat_owner_id_check CHECK (owner_id IS NOT NULL);'
);

SELECT public.create_constraint(
    'flat',
    'flat_price_check',
    'ALTER TABLE public.flat ADD CONSTRAINT flat_price_check CHECK (price > 0 AND price IS NOT NULL);'
);

SELECT public.create_constraint(
    'flat',
    'flat_rooms_check',
    'ALTER TABLE public.flat ADD CONSTRAINT flat_rooms_check CHECK (rooms > 0 AND rooms IS NOT NULL);'
);

SELECT public.create_constraint(
    'flat',
    'flat_square_check',
    'ALTER TABLE public.flat ADD CONSTRAINT flat_square_check CHECK (square > 0 AND square IS NOT NULL);'
);

SELECT public.create_constraint(
    'flat',
    'flat_address_check',
    'ALTER TABLE public.flat ADD CONSTRAINT flat_address_check CHECK (address IS NOT NULL);'
);

SELECT public.create_constraint(
    'flat',
    'flat_floor_check',
    'ALTER TABLE public.flat ADD CONSTRAINT flat_floor_check CHECK (floor >= 0);'
);

SELECT public.create_constraint(
    'flat',
    'flat_max_floor_check',
    'ALTER TABLE public.flat ADD CONSTRAINT flat_max_floor_check CHECK (max_floor >= 0 AND max_floor >= floor);'
);


-- create constraints to public.flat_photo
SELECT public.create_constraint (
    'flat',
    'flat_photo_flat_id_fkey',
    'ALTER TABLE public.flat_photo ADD CONSTRAINT flat_photo_flat_id_fkey FOREIGN KEY (flat_id) REFERENCES public.flat (id);'
);

SELECT public.create_constraint (
    'flat_photo',
    'flat_photo_flat_id_check',
    'ALTER TABLE public.flat_photo ADD CONSTRAINT flat_photo_flat_id_check CHECK (flat_id IS NOT NULL);'
);

SELECT public.create_constraint(
    'flat_photo',
    'flat_photo_check',
    'ALTER TABLE public.flat_photo ADD CONSTRAINT flat_photo_check CHECK (photo IS NOT NULL);'
);


-- create constrains to public.neighborhood
SELECT public.create_constraint (
    'neighborhood',
    'neighborhood_pkey',
    'ALTER TABLE public.neighborhood ADD CONSTRAINT neighborhood_pkey PRIMARY KEY (id);'
);

SELECT public.create_constraint (
    'tenant',
    'neighborhood_tenant_id_fkey',
    'ALTER TABLE public.neighborhood ADD CONSTRAINT neighborhood_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.tenant (id);'
);

SELECT public.create_constraint (
    'neighborhood',
    'neighborhood_tenant_id_check',
    'ALTER TABLE public.neighborhood ADD CONSTRAINT neighborhood_tenant_id_check CHECK (tenant_id IS NOT NULL);'
);

SELECT public.create_constraint(
    'neighborhood',
    'neighborhood_neighbors_check',
    'ALTER TABLE public.neighborhood ADD CONSTRAINT neighborhood_neighbors_check CHECK (neighbors > 0 AND neighbors IS NOT NULL);'
);

SELECT public.create_constraint(
    'neighborhood',
    'neighborhood_price_check',
    'ALTER TABLE public.neighborhood ADD CONSTRAINT neighborhood_price_check CHECK (price > 0 AND price IS NOT NULL);'
);

SELECT public.create_constraint(
    'neighborhood',
    'neighborhood_sex_check',
    'ALTER TABLE public.neighborhood ADD CONSTRAINT neighborhood_sex_check CHECK (sex IN (''M'', ''F'', ''N'') AND sex IS NOT NULL);'
);


-- create constraints to public.goods
SELECT public.create_constraint (
    'goods',
    'goods_pkey',
    'ALTER TABLE public.goods ADD CONSTRAINT goods_pkey PRIMARY KEY (id);'
);

SELECT public.create_constraint (
    'tenant',
    'goods_owner_id_fkey',
    'ALTER TABLE public.goods ADD CONSTRAINT goods_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public.tenant (id);'
);

SELECT public.create_constraint (
    'goods',
    'goods_owner_id_check',
    'ALTER TABLE public.goods ADD CONSTRAINT goods_owner_id_check CHECK (owner_id IS NOT NULL);'
);
SELECT public.create_constraint(
    'goods',
    'goods_name_check',
    'ALTER TABLE public.goods ADD CONSTRAINT goods_name_check CHECK (name IS NOT NULL);'
);

SELECT public.create_constraint(
    'goods',
    'goods_price_check',
    'ALTER TABLE public.goods ADD CONSTRAINT goods_price_check CHECK (price > 0 AND price IS NOT NULL);'
);

-- E - excellent
-- G - good
-- S - satisfactory
-- U - unsatisfactory
-- T - terrible
SELECT public.create_constraint(
    'goods',
    'goods_condition_check',
    'ALTER TABLE public.goods ADD CONSTRAINT goods_condition_check CHECK ' ||
    '(condition IN (''E'', ''G'', ''S'', ''U'', ''T'') AND condition IS NOT NULL);'
);


-- create constraints to public.subscription_landlord
SELECT public.create_constraint (
    'tenant',
    'subscription_landlord_tenant_id_fkey',
    'ALTER TABLE public.subscription_landlord ADD CONSTRAINT subscription_landlord_tenant_id_fkey' ||
    ' FOREIGN KEY (tenant_id) REFERENCES public.tenant (id);'
);

SELECT public.create_constraint (
    'subscription_landlord',
    'subscription_landlord_tenant_id_check',
    'ALTER TABLE public.subscription_landlord ADD CONSTRAINT subscription_landlord_tenant_id_check' ||
    ' CHECK (tenant_id IS NOT NULL);'
);

SELECT public.create_constraint (
    'landlord',
    'subscription_landlord_id_fkey',
    'ALTER TABLE public.subscription_landlord ADD CONSTRAINT subscription_landlord_id_fkey' ||
    ' FOREIGN KEY (landlord_id) REFERENCES public.landlord (id);'
);

SELECT public.create_constraint (
    'subscription_landlord',
    'subscription_landlord_id_check',
    'ALTER TABLE public.subscription_landlord ADD CONSTRAINT subscription_landlord_id_check' ||
    ' CHECK (landlord_id IS NOT NULL);'
);


-- create constraints to public.likes_flat
SELECT public.create_constraint (
    'tenant',
    'likes_flat_tenant_id_fkey',
    'ALTER TABLE public.likes_flat ADD CONSTRAINT likes_flat_tenant_id_fkey' ||
          ' FOREIGN KEY (tenant_id) REFERENCES public.tenant (id);'
);

SELECT public.create_constraint (
    'likes_flat',
    'likes_flat_tenant_id_check',
    'ALTER TABLE public.likes_flat ADD CONSTRAINT likes_flat_tenant_id_check CHECK (tenant_id IS NOT NULL);'
);

SELECT public.create_constraint (
    'flat',
    'likes_flat_id_fkey',
    'ALTER TABLE public.likes_flat ADD CONSTRAINT likes_flat_id_fkey' ||
    ' FOREIGN KEY (flat_id) REFERENCES public.flat (id);'
);

SELECT public.create_constraint (
    'likes_flat',
    'likes_flat_id_check',
    'ALTER TABLE public.likes_flat ADD CONSTRAINT likes_flat_id_check CHECK (flat_id IS NOT NULL);'
);


-- create constraints to public.subscription_flat
SELECT public.create_constraint (
    'tenant',
    'subscription_flat_tenant_id_fkey',
    'ALTER TABLE public.subscription_flat ADD CONSTRAINT subscription_flat_tenant_id_fkey' ||
    ' FOREIGN KEY (tenant_id) REFERENCES public.tenant (id);'
);

SELECT public.create_constraint (
    'subscription_flat',
    'subscription_flat_tenant_id_check',
    'ALTER TABLE public.subscription_flat ADD CONSTRAINT subscription_flat_tenant_id_check' ||
    ' CHECK (tenant_id IS NOT NULL);'
);

SELECT public.create_constraint(
    'subscription_flat',
    'subscription_flat_price_check',
    'ALTER TABLE public.subscription_flat ADD CONSTRAINT subscription_flat_price_check' ||
    ' CHECK (min_price <= max_price AND min_price >= 0);'
);

SELECT public.create_constraint(
    'subscription_flat',
    'subscription_flat_rooms_check',
    'ALTER TABLE public.subscription_flat ADD CONSTRAINT subscription_flat_rooms_check' ||
    ' CHECK (min_rooms <= max_rooms AND min_rooms >= 0);'
);

SELECT public.create_constraint(
    'subscription_flat',
    'subscription_flat_square_check',
    'ALTER TABLE public.subscription_flat ADD CONSTRAINT subscription_flat_square_check' ||
    ' CHECK (min_square <= max_square AND min_square >= 0);'
);
