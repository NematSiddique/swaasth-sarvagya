CREATE TABLE patient_tests
(
  patient_id INTEGER REFERENCES patients(id),
  test_name VARCHAR(255),
  status VARCHAR(50) DEFAULT 'Ordered',
  ordered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY
  (patient_id, test_name)
);