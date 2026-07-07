CREATE TABLE medicine_groups
(
  id SERIAL PRIMARY KEY,
  group_name VARCHAR(255) UNIQUE
);
CREATE INDEX ix_medicine_groups_group_name ON medicine_groups (group_name);