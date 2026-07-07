CREATE TABLE nurses
(
  id SERIAL PRIMARY KEY,
  hospital_id INTEGER REFERENCES hospitals(id),
  name VARCHAR(255),
  shift VARCHAR(100),
  attendance_status VARCHAR(100),
  leave_status VARCHAR(100)
);
CREATE INDEX ix_nurses_hospital_id ON nurses (hospital_id);