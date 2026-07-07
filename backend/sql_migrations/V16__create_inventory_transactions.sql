CREATE TABLE inventory_transactions
(
  id SERIAL PRIMARY KEY,
  hospital_id INTEGER REFERENCES hospitals(id),
  medicine_id INTEGER REFERENCES medicines(id),
  quantity INTEGER,
  transaction_type VARCHAR(50),
  source_hospital_id INTEGER REFERENCES hospitals(id),
  destination_hospital_id INTEGER REFERENCES hospitals(id),
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX ix_inventory_transactions_hospital_id ON inventory_transactions (hospital_id);
CREATE INDEX ix_inventory_transactions_medicine_id ON inventory_transactions (medicine_id);