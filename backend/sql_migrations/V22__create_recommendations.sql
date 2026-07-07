CREATE TABLE recommendations
(
  id SERIAL PRIMARY KEY,
  alert_id INTEGER REFERENCES alerts(id),
  recommendation TEXT,
  reason TEXT,
  priority INTEGER DEFAULT 1,
  accepted BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);