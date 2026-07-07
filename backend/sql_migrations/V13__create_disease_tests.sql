CREATE TABLE disease_tests
(
  disease_id INTEGER REFERENCES diseases(id),
  test_name VARCHAR(255),
  priority INTEGER DEFAULT 1,
  PRIMARY KEY (disease_id, test_name)
);