-- trigger to delete flats before deleting landlord
CREATE OR REPLACE FUNCTION public.delete_tenant_flats ()
RETURNS TRIGGER AS
$$
BEGIN
    DELETE FROM public.flat
    WHERE owner_id = old.id;
    return old;
END;
$$
LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS delete_landlord on public.landlord;

CREATE TRIGGER delete_landlord
BEFORE DELETE on public.landlord
FOR EACH ROW
EXECUTE PROCEDURE public.delete_tenant_flats();


-- trigger to delete flats photos before deleting flat
CREATE OR REPLACE FUNCTION public.delete_flat_photos ()
RETURNS TRIGGER AS
$$
BEGIN
    DELETE FROM public.flat_photo
    WHERE flat_id = old.id;
    return old;
END;
$$
LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS delete_flat on public.flat;

CREATE TRIGGER delete_flat
BEFORE DELETE on public.flat
FOR EACH ROW
EXECUTE PROCEDURE public.delete_flat_photos();


-- trigger to delete neighborhoods and goods before deleting tenant
CREATE OR REPLACE FUNCTION public.delete_tenant_dependencies ()
RETURNS TRIGGER AS
$$
BEGIN
    DELETE FROM public.neighborhood WHERE tenant_id = old.id;
    DELETE FROM public.goods WHERE owner_id = old.id;
    return old;
END;
$$
LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS delete_tenant on public.tenant;

CREATE TRIGGER delete_tenant
BEFORE DELETE on public.tenant
FOR EACH ROW
EXECUTE PROCEDURE public.delete_tenant_dependencies();
