CREATE TABLE alerts
(
  id SERIAL PRIMARY KEY,
  hospital_id INTEGER REFERENCES hospitals(id),
  alert_type VARCHAR(100),
  severity VARCHAR(50),
  message TEXT,
  resolved BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX ix_alerts_hospital_id ON alerts (hospital_id);
CREATE INDEX ix_alerts_alert_type ON alerts (alert_type);
CREATE INDEX ix_alerts_severity ON alerts (severity);