CREATE TABLE supplier_medicines
(
  supplier_id INTEGER REFERENCES suppliers(id),
  medicine_id INTEGER REFERENCES medicines(id),
  PRIMARY KEY (supplier_id, medicine_id)
);