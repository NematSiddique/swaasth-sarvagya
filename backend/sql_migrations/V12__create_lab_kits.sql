CREATE TABLE lab_kits
(
  id SERIAL PRIMARY KEY,
  laboratory_id INTEGER REFERENCES laboratories(id),
  test_name VARCHAR(255),
  stock INTEGER DEFAULT 0,
  threshold INTEGER DEFAULT 0
);
CREATE INDEX ix_lab_kits_laboratory_id ON lab_kits (laboratory_id);
CREATE INDEX ix_lab_kits_test_name ON lab_kits (test_name);