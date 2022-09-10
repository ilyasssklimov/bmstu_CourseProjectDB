-- trigger to delete flats and subscriptions before deleting landlord
CREATE OR REPLACE FUNCTION public.delete_landlord_dependencies ()
RETURNS TRIGGER AS
$$
BEGIN
    UPDATE public.flat SET owner_id = NULL WHERE owner_id = old.id;
    DELETE FROM public.subscription_landlord WHERE landlord_id = old.id;
    RETURN old;
END;
$$
LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS delete_landlord on public.landlord;

CREATE TRIGGER delete_landlord
BEFORE DELETE on public.landlord
FOR EACH ROW
EXECUTE PROCEDURE public.delete_landlord_dependencies();


-- trigger to delete flats photos before deleting flat
CREATE OR REPLACE FUNCTION public.delete_flat_dependencies ()
RETURNS TRIGGER AS
$$
BEGIN
    DELETE FROM public.flat_photo WHERE flat_id = old.id;
    DELETE FROM public.likes_flat WHERE flat_id = old.id;
    RETURN old;
END;
$$
LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS delete_flat on public.flat;

CREATE TRIGGER delete_flat
BEFORE DELETE on public.flat
FOR EACH ROW
EXECUTE PROCEDURE public.delete_flat_dependencies();


-- trigger to delete neighborhoods, goods, subscriptions and likes before deleting tenant
CREATE OR REPLACE FUNCTION public.delete_tenant_dependencies ()
RETURNS TRIGGER AS
$$
BEGIN
    UPDATE public.neighborhood SET tenant_id = NULL WHERE tenant_id = old.id;
    UPDATE public.goods SET owner_id = NULL WHERE owner_id = old.id;
    DELETE FROM public.subscription_landlord WHERE tenant_id = old.id;
    DELETE FROM public.likes_flat WHERE tenant_id = old.id;
    DELETE FROM public.subscription_flat WHERE tenant_id = old.id;
    RETURN old;
END;
$$
LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS delete_tenant on public.tenant;

CREATE TRIGGER delete_tenant
BEFORE DELETE on public.tenant
FOR EACH ROW
EXECUTE PROCEDURE public.delete_tenant_dependencies();


-- trigger to delete metro before deleting subscription_flat
CREATE OR REPLACE FUNCTION public.delete_subscription_metro ()
RETURNS TRIGGER AS
$$
BEGIN
    DELETE FROM public.subscription_metro WHERE tenant_id = old.tenant_id;
    RETURN old;
END;
$$
LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS delete_subscription_flat on public.subscription_flat;

CREATE TRIGGER delete_subscription_flat
BEFORE DELETE on public.subscription_flat
FOR EACH ROW
EXECUTE PROCEDURE public.delete_subscription_metro();


-- trigger to delete subscription_flat before inserting subscription_flat
CREATE OR REPLACE FUNCTION public.delete_flat_subscription ()
RETURNS TRIGGER AS
$$
BEGIN
    DELETE FROM public.subscription_flat WHERE tenant_id = new.tenant_id;
    RETURN new;
END;
$$
LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS insert_subscription_flat on public.subscription_flat;

CREATE TRIGGER insert_subscription_flat
BEFORE INSERT on public.subscription_flat
FOR EACH ROW
EXECUTE PROCEDURE public.delete_flat_subscription();
