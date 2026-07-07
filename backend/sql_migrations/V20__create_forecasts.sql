CREATE TABLE forecasts
(
  id SERIAL PRIMARY KEY,
  hospital_id INTEGER REFERENCES hospitals(id),
  forecast_type VARCHAR(100),
  target VARCHAR(255),
  predicted_value FLOAT,
  confidence FLOAT,
  model_name VARCHAR(100),
  generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  forecast_for DATE
);
CREATE INDEX ix_forecasts_hospital_id ON forecasts (hospital_id);
CREATE INDEX ix_forecasts_forecast_type ON forecasts (forecast_type);
CREATE INDEX ix_forecasts_target ON forecasts (target);
CREATE INDEX ix_forecasts_forecast_for ON forecasts (forecast_for);