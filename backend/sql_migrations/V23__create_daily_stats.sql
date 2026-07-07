CREATE TABLE daily_patient_stats
(
  hospital_id INTEGER REFERENCES hospitals(id),
  date DATE,
  total_patients INTEGER DEFAULT 0,
  disease_counts JSON,
  admissions INTEGER DEFAULT 0,
  discharges INTEGER DEFAULT 0,
  PRIMARY KEY (hospital_id, date)
);

CREATE TABLE daily_inventory_usage
(
  hospital_id INTEGER REFERENCES hospitals(id),
  medicine_id INTEGER REFERENCES medicines(id),
  date DATE,
  used_today INTEGER DEFAULT 0,
  remaining INTEGER DEFAULT 0,
  forecast FLOAT,
  PRIMARY KEY (hospital_id, medicine_id, date)
);

CREATE TABLE daily_bed_stats
(
  hospital_id INTEGER REFERENCES hospitals(id),
  date DATE,
  occupied INTEGER DEFAULT 0,
  available INTEGER DEFAULT 0,
  admissions INTEGER DEFAULT 0,
  discharges INTEGER DEFAULT 0,
  PRIMARY KEY (hospital_id, date)
);

CREATE TABLE daily_doctor_stats
(
  doctor_id INTEGER REFERENCES doctors(id),
  date DATE,
  patients_seen INTEGER DEFAULT 0,
  attendance BOOLEAN DEFAULT TRUE,
  hours_worked FLOAT,
  PRIMARY KEY (doctor_id, date)
);