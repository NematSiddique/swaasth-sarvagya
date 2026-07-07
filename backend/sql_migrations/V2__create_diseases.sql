CREATE TABLE diseases
(
  id SERIAL PRIMARY KEY,
  disease_name VARCHAR(255) UNIQUE,
  category VARCHAR(255),
  seasonal BOOLEAN DEFAULT FALSE,
  description TEXT,
  seasonal_trends JSON,
  weather_correlation JSON,
  demographic_risk JSON
);
CREATE INDEX ix_diseases_disease_name ON diseases (disease_name);