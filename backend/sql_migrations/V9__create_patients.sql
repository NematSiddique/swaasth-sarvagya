CREATE TABLE patients
(
  id SERIAL PRIMARY KEY,
  hospital_id INTEGER REFERENCES hospitals(id),
  doctor_id INTEGER REFERENCES doctors(id),
  disease_id INTEGER REFERENCES diseases(id),
  age INTEGER,
  gender VARCHAR(50),
  severity VARCHAR(50),
  bed_required BOOLEAN DEFAULT FALSE,
  bed_allocated BOOLEAN DEFAULT FALSE,
  admission_status VARCHAR(50),
  registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  discharged_at TIMESTAMP
);
CREATE INDEX ix_patients_hospital_id ON patients (hospital_id);
CREATE INDEX ix_patients_severity ON patients (severity);
CREATE INDEX ix_patients_admission_status ON patients (admission_status);