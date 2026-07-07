CREATE TABLE doctor_attendance
(
  doctor_id INTEGER REFERENCES doctors(id),
  date DATE,
  status BOOLEAN DEFAULT TRUE,
  hours_worked FLOAT,
  PRIMARY KEY (doctor_id, date)
);