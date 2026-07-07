CREATE TABLE doctors
(
  id SERIAL PRIMARY KEY,
  hospital_id INTEGER REFERENCES hospitals(id),
  name VARCHAR(255),
  specialization VARCHAR(255),
  shift VARCHAR(100),
  leave_status VARCHAR(100),
  consultation_count INTEGER DEFAULT 0
);
CREATE INDEX ix_doctors_hospital_id ON doctors (hospital_id);
CREATE INDEX ix_doctors_specialization ON doctors (specialization);