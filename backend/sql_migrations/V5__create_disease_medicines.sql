CREATE TABLE disease_medicines
(
  disease_id INTEGER REFERENCES diseases(id),
  medicine_id INTEGER REFERENCES medicines(id),
  priority INTEGER DEFAULT 1,
  PRIMARY KEY (disease_id, medicine_id)
);