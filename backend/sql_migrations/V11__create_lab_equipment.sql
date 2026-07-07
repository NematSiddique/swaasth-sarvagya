CREATE TABLE lab_equipment
(
  id SERIAL PRIMARY KEY,
  laboratory_id INTEGER REFERENCES laboratories(id),
  equipment_name VARCHAR(255),
  status VARCHAR(100) DEFAULT 'Available',
  last_service DATE,
  expected_life INTEGER,
  usage_frequency INTEGER,
  machine_age INTEGER
);
CREATE INDEX ix_lab_equipment_laboratory_id ON lab_equipment (laboratory_id);