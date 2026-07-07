CREATE TABLE beds
(
  id SERIAL PRIMARY KEY,
  hospital_id INTEGER REFERENCES hospitals(id),
  bed_type VARCHAR(100) DEFAULT 'General',
  occupied BOOLEAN DEFAULT FALSE,
  patient_id INTEGER REFERENCES patients(id)
);
CREATE INDEX ix_beds_hospital_id ON beds (hospital_id);
CREATE INDEX ix_beds_bed_type ON beds (bed_type);