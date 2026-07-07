CREATE TABLE laboratories
(
  id SERIAL PRIMARY KEY,
  hospital_id INTEGER REFERENCES hospitals(id),
  name VARCHAR(255),
  status VARCHAR(100)
);
CREATE INDEX ix_laboratories_hospital_id ON laboratories (hospital_id);