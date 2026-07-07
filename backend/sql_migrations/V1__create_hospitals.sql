CREATE TABLE hospitals
(
  id SERIAL PRIMARY KEY,
  name VARCHAR(255),
  district VARCHAR(255),
  type VARCHAR(50),
  latitude FLOAT,
  longitude FLOAT,
  total_beds INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX ix_hospitals_name ON hospitals (name);
CREATE INDEX ix_hospitals_district ON hospitals (district);