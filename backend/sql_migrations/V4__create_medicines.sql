CREATE TABLE medicines
(
  id SERIAL PRIMARY KEY,
  group_id INTEGER REFERENCES medicine_groups(id),
  generic_name VARCHAR(255),
  brand_name VARCHAR(255),
  dosage VARCHAR(100)
);
CREATE INDEX ix_medicines_generic_name ON medicines (generic_name);
CREATE INDEX ix_medicines_brand_name ON medicines (brand_name);