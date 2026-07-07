CREATE TABLE inventory
(
  id SERIAL PRIMARY KEY,
  hospital_id INTEGER REFERENCES hospitals(id),
  medicine_id INTEGER REFERENCES medicines(id),
  quantity INTEGER DEFAULT 0,
  expiry_date DATE,
  reorder_level INTEGER DEFAULT 0,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE
  (hospital_id, medicine_id)
);
CREATE INDEX ix_inventory_hospital_id ON inventory (hospital_id);
CREATE INDEX ix_inventory_medicine_id ON inventory (medicine_id);
CREATE INDEX ix_inventory_expiry_date ON inventory (expiry_date);