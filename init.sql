CREATE TABLE vehicle_brands (
  vehicle_brand char(20),
  vehicle_brand_id int
);

CREATE TABLE vehicle_categories (
  vehicle_category char(35),
  vehicle_category_id int
);

CREATE TABLE vehicles (
  vehicle_id int,
  vehicle_brand_id int,
  vehicle_category_id int,
  vehicle_model char(20)
);

CREATE TABLE part_categories (
  part_category text,
  part_category_id int
);

CREATE TABLE parts (
  part_id int,
  part_site_id int,
  part_name char(30),
  part_category_id int,
  vehicle_id int
);

CREATE VIEW parts_v AS
SELECT
  vehicle_brand,
  vehicle_category,
  vehicle_model,
  part_name,
  part_category,
  part_site_id,
  part_id
FROM parts
LEFT JOIN part_categories ON part_categories.part_category_id = parts.part_category_id
LEFT JOIN vehicles ON vehicles.vehicle_id = parts.vehicle_id
LEFT JOIN vehicle_categories ON vehicle_categories.vehicle_category_id = vehicles.vehicle_category_id
LEFT JOIN vehicle_brands ON vehicle_brands.vehicle_brand_id = vehicles.vehicle_brand_id
