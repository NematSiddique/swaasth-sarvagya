-- Seed data for local forecasting and alerting demos.
-- This data creates one district hospital with enough history and live state
-- to trigger both forecast generation and alert conditions.

INSERT INTO hospitals (id, name, district, type, latitude, longitude, total_beds, created_at)
VALUES
  (1001, 'Mock District Hospital', 'Mock District', 'District', 18.5204, 73.8567, 100, CURRENT_TIMESTAMP)
ON CONFLICT (id) DO NOTHING;

INSERT INTO diseases (id, disease_name, category, seasonal, description)
VALUES
  (2001, 'Dengue', 'Vector-borne', TRUE, 'Seasonal mock disease used for outbreak simulation')
ON CONFLICT (id) DO NOTHING;

INSERT INTO medicine_groups (id, group_name)
VALUES
  (3001, 'Essential Medicines')
ON CONFLICT (id) DO NOTHING;

INSERT INTO medicines (id, group_id, generic_name, brand_name, dosage)
VALUES
  (4001, 3001, 'Paracetamol', 'MediCalm', '500 mg'),
  (4002, 3001, 'Amoxicillin', 'AmoxiCare', '250 mg')
ON CONFLICT (id) DO NOTHING;

INSERT INTO doctors (id, hospital_id, name, specialization, shift, leave_status, consultation_count)
VALUES
  (5001, 1001, 'Dr. Mock Sharma', 'General Medicine', 'Day', 'Available', 42),
  (5002, 1001, 'Dr. I. Example', 'Pediatrics', 'Night', 'Available', 18)
ON CONFLICT (id) DO NOTHING;

INSERT INTO doctor_attendance (doctor_id, date, status, hours_worked)
VALUES
  (5001, CURRENT_DATE, FALSE, 0),
  (5002, CURRENT_DATE, TRUE, 8)
ON CONFLICT (doctor_id, date) DO NOTHING;

INSERT INTO laboratories (id, hospital_id, name, status)
VALUES
  (6001, 1001, 'Central Lab', 'Maintenance'),
  (6002, 1001, 'Biochemistry Lab', 'Operational')
ON CONFLICT (id) DO NOTHING;

INSERT INTO lab_equipment (id, laboratory_id, equipment_name, status, last_service, expected_life, usage_frequency, machine_age)
VALUES
  (7001, 6001, 'CBC Analyzer', 'Needs Service', CURRENT_DATE - 220, 7, 40, 6),
  (7002, 6002, 'Chemistry Analyzer', 'Available', CURRENT_DATE - 30, 8, 20, 2)
ON CONFLICT (id) DO NOTHING;

INSERT INTO lab_kits (id, laboratory_id, test_name, stock, threshold)
VALUES
  (8001, 6001, 'Dengue Rapid Test', 3, 12),
  (8002, 6002, 'Malaria Rapid Test', 24, 10)
ON CONFLICT (id) DO NOTHING;

INSERT INTO patients (
  id, hospital_id, doctor_id, disease_id, age, gender, severity,
  bed_required, bed_allocated, admission_status, registered_at, discharged_at
)
VALUES
  (9001, 1001, 5001, 2001, 34, 'M', 'Moderate', FALSE, FALSE, 'active', CURRENT_TIMESTAMP - INTERVAL '0 days', NULL),
  (9002, 1001, 5001, 2001, 35, 'F', 'Moderate', FALSE, FALSE, 'active', CURRENT_TIMESTAMP - INTERVAL '1 days', NULL),
  (9003, 1001, 5001, 2001, 36, 'M', 'Moderate', FALSE, FALSE, 'active', CURRENT_TIMESTAMP - INTERVAL '2 days', NULL),
  (9004, 1001, 5001, 2001, 37, 'F', 'Moderate', FALSE, FALSE, 'active', CURRENT_TIMESTAMP - INTERVAL '3 days', NULL),
  (9005, 1001, 5001, 2001, 38, 'M', 'Moderate', FALSE, FALSE, 'active', CURRENT_TIMESTAMP - INTERVAL '4 days', NULL),
  (9006, 1001, 5001, 2001, 39, 'F', 'Moderate', FALSE, FALSE, 'active', CURRENT_TIMESTAMP - INTERVAL '5 days', NULL),
  (9007, 1001, 5001, 2001, 40, 'M', 'Moderate', FALSE, FALSE, 'active', CURRENT_TIMESTAMP - INTERVAL '6 days', NULL),
  (9008, 1001, 5001, 2001, 41, 'F', 'Moderate', FALSE, FALSE, 'active', CURRENT_TIMESTAMP - INTERVAL '7 days', NULL),
  (9009, 1001, 5001, 2001, 42, 'M', 'Moderate', FALSE, FALSE, 'active', CURRENT_TIMESTAMP - INTERVAL '8 days', NULL),
  (9010, 1001, 5001, 2001, 43, 'F', 'Moderate', FALSE, FALSE, 'active', CURRENT_TIMESTAMP - INTERVAL '9 days', NULL)
ON CONFLICT (id) DO NOTHING;

INSERT INTO beds (id, hospital_id, bed_type, occupied, patient_id)
VALUES
  (10001, 1001, 'General', TRUE, 9001),
  (10002, 1001, 'General', TRUE, 9002),
  (10003, 1001, 'General', TRUE, 9003),
  (10004, 1001, 'General', TRUE, 9004),
  (10005, 1001, 'General', TRUE, 9005),
  (10006, 1001, 'General', TRUE, 9006),
  (10007, 1001, 'General', TRUE, 9007),
  (10008, 1001, 'General', TRUE, 9008),
  (10009, 1001, 'General', TRUE, 9009),
  (10010, 1001, 'General', TRUE, 9010),
  (10011, 1001, 'General', TRUE, NULL),
  (10012, 1001, 'General', TRUE, NULL),
  (10013, 1001, 'General', TRUE, NULL),
  (10014, 1001, 'General', TRUE, NULL),
  (10015, 1001, 'General', TRUE, NULL),
  (10016, 1001, 'General', TRUE, NULL),
  (10017, 1001, 'General', TRUE, NULL),
  (10018, 1001, 'General', TRUE, NULL),
  (10019, 1001, 'General', TRUE, NULL),
  (10020, 1001, 'General', TRUE, NULL),
  (10021, 1001, 'General', TRUE, NULL),
  (10022, 1001, 'General', TRUE, NULL),
  (10023, 1001, 'General', TRUE, NULL),
  (10024, 1001, 'General', TRUE, NULL),
  (10025, 1001, 'General', TRUE, NULL),
  (10026, 1001, 'General', TRUE, NULL),
  (10027, 1001, 'General', TRUE, NULL),
  (10028, 1001, 'General', TRUE, NULL),
  (10029, 1001, 'General', TRUE, NULL),
  (10030, 1001, 'General', TRUE, NULL),
  (10031, 1001, 'General', TRUE, NULL),
  (10032, 1001, 'General', TRUE, NULL),
  (10033, 1001, 'General', TRUE, NULL),
  (10034, 1001, 'General', TRUE, NULL),
  (10035, 1001, 'General', TRUE, NULL),
  (10036, 1001, 'General', TRUE, NULL),
  (10037, 1001, 'General', TRUE, NULL),
  (10038, 1001, 'General', TRUE, NULL),
  (10039, 1001, 'General', TRUE, NULL),
  (10040, 1001, 'General', TRUE, NULL),
  (10041, 1001, 'General', TRUE, NULL),
  (10042, 1001, 'General', TRUE, NULL),
  (10043, 1001, 'General', TRUE, NULL),
  (10044, 1001, 'General', TRUE, NULL),
  (10045, 1001, 'General', TRUE, NULL),
  (10046, 1001, 'General', TRUE, NULL),
  (10047, 1001, 'General', TRUE, NULL),
  (10048, 1001, 'General', TRUE, NULL),
  (10049, 1001, 'General', TRUE, NULL),
  (10050, 1001, 'General', TRUE, NULL),
  (10051, 1001, 'General', TRUE, NULL),
  (10052, 1001, 'General', TRUE, NULL),
  (10053, 1001, 'General', TRUE, NULL),
  (10054, 1001, 'General', TRUE, NULL),
  (10055, 1001, 'General', TRUE, NULL),
  (10056, 1001, 'General', TRUE, NULL),
  (10057, 1001, 'General', TRUE, NULL),
  (10058, 1001, 'General', TRUE, NULL),
  (10059, 1001, 'General', TRUE, NULL),
  (10060, 1001, 'General', TRUE, NULL),
  (10061, 1001, 'General', TRUE, NULL),
  (10062, 1001, 'General', TRUE, NULL),
  (10063, 1001, 'General', TRUE, NULL),
  (10064, 1001, 'General', TRUE, NULL),
  (10065, 1001, 'General', TRUE, NULL),
  (10066, 1001, 'General', TRUE, NULL),
  (10067, 1001, 'General', TRUE, NULL),
  (10068, 1001, 'General', TRUE, NULL),
  (10069, 1001, 'General', TRUE, NULL),
  (10070, 1001, 'General', TRUE, NULL),
  (10071, 1001, 'General', TRUE, NULL),
  (10072, 1001, 'General', TRUE, NULL),
  (10073, 1001, 'General', TRUE, NULL),
  (10074, 1001, 'General', TRUE, NULL),
  (10075, 1001, 'General', TRUE, NULL),
  (10076, 1001, 'General', TRUE, NULL),
  (10077, 1001, 'General', TRUE, NULL),
  (10078, 1001, 'General', TRUE, NULL),
  (10079, 1001, 'General', TRUE, NULL),
  (10080, 1001, 'General', TRUE, NULL),
  (10081, 1001, 'General', TRUE, NULL),
  (10082, 1001, 'General', TRUE, NULL),
  (10083, 1001, 'General', TRUE, NULL),
  (10084, 1001, 'General', TRUE, NULL),
  (10085, 1001, 'General', TRUE, NULL),
  (10086, 1001, 'General', TRUE, NULL),
  (10087, 1001, 'General', TRUE, NULL),
  (10088, 1001, 'General', TRUE, NULL),
  (10089, 1001, 'General', TRUE, NULL),
  (10090, 1001, 'General', TRUE, NULL),
  (10091, 1001, 'General', TRUE, NULL)
ON CONFLICT (id) DO NOTHING;

INSERT INTO inventory (id, hospital_id, medicine_id, quantity, expiry_date, reorder_level, updated_at)
VALUES
  (11001, 1001, 4001, 8, CURRENT_DATE + 10, 20, CURRENT_TIMESTAMP),
  (11002, 1001, 4002, 50, CURRENT_DATE + 75, 15, CURRENT_TIMESTAMP)
ON CONFLICT (id) DO NOTHING;

INSERT INTO patient_tests (patient_id, test_name, status, ordered_at)
VALUES
  (9001, 'Dengue Rapid Test', 'completed', CURRENT_TIMESTAMP - INTERVAL '0 days'),
  (9002, 'Dengue Rapid Test', 'completed', CURRENT_TIMESTAMP - INTERVAL '1 days'),
  (9003, 'Dengue Rapid Test', 'completed', CURRENT_TIMESTAMP - INTERVAL '2 days'),
  (9004, 'Dengue Rapid Test', 'completed', CURRENT_TIMESTAMP - INTERVAL '3 days'),
  (9005, 'Dengue Rapid Test', 'completed', CURRENT_TIMESTAMP - INTERVAL '4 days'),
  (9006, 'Dengue Rapid Test', 'completed', CURRENT_TIMESTAMP - INTERVAL '5 days'),
  (9007, 'Dengue Rapid Test', 'completed', CURRENT_TIMESTAMP - INTERVAL '6 days'),
  (9008, 'Dengue Rapid Test', 'completed', CURRENT_TIMESTAMP - INTERVAL '7 days'),
  (9009, 'Dengue Rapid Test', 'completed', CURRENT_TIMESTAMP - INTERVAL '8 days'),
  (9010, 'Dengue Rapid Test', 'completed', CURRENT_TIMESTAMP - INTERVAL '9 days')
ON CONFLICT (patient_id, test_name) DO NOTHING;

INSERT INTO daily_inventory_usage (hospital_id, medicine_id, date, used_today, remaining, forecast)
VALUES
  (1001, 4001, CURRENT_DATE - 9, 6, 94, NULL),
  (1001, 4001, CURRENT_DATE - 8, 7, 87, NULL),
  (1001, 4001, CURRENT_DATE - 7, 8, 79, NULL),
  (1001, 4001, CURRENT_DATE - 6, 7, 72, NULL),
  (1001, 4001, CURRENT_DATE - 5, 8, 64, NULL),
  (1001, 4001, CURRENT_DATE - 4, 9, 55, NULL),
  (1001, 4001, CURRENT_DATE - 3, 6, 49, NULL),
  (1001, 4001, CURRENT_DATE - 2, 7, 42, NULL),
  (1001, 4001, CURRENT_DATE - 1, 8, 34, NULL),
  (1001, 4001, CURRENT_DATE, 7, 27, NULL),
  (1001, 4002, CURRENT_DATE - 9, 2, 98, NULL),
  (1001, 4002, CURRENT_DATE - 8, 3, 95, NULL),
  (1001, 4002, CURRENT_DATE - 7, 2, 93, NULL),
  (1001, 4002, CURRENT_DATE - 6, 4, 89, NULL),
  (1001, 4002, CURRENT_DATE - 5, 3, 86, NULL),
  (1001, 4002, CURRENT_DATE - 4, 4, 82, NULL),
  (1001, 4002, CURRENT_DATE - 3, 3, 79, NULL),
  (1001, 4002, CURRENT_DATE - 2, 2, 77, NULL),
  (1001, 4002, CURRENT_DATE - 1, 4, 73, NULL),
  (1001, 4002, CURRENT_DATE, 3, 70, NULL)
ON CONFLICT (hospital_id, medicine_id, date) DO NOTHING;

INSERT INTO daily_bed_stats (hospital_id, date, occupied, available, admissions, discharges)
VALUES
  (1001, CURRENT_DATE - 9, 84, 16, 6, 4),
  (1001, CURRENT_DATE - 8, 86, 14, 7, 5),
  (1001, CURRENT_DATE - 7, 87, 13, 5, 4),
  (1001, CURRENT_DATE - 6, 89, 11, 7, 5),
  (1001, CURRENT_DATE - 5, 88, 12, 6, 4),
  (1001, CURRENT_DATE - 4, 90, 10, 8, 6),
  (1001, CURRENT_DATE - 3, 91, 9, 7, 5),
  (1001, CURRENT_DATE - 2, 92, 8, 8, 6),
  (1001, CURRENT_DATE - 1, 91, 9, 7, 8),
  (1001, CURRENT_DATE, 91, 9, 6, 5)
ON CONFLICT (hospital_id, date) DO NOTHING;

INSERT INTO forecasts (id, hospital_id, forecast_type, target, predicted_value, confidence, model_name, generated_at, forecast_for)
VALUES
  (12001, 1001, 'bed_occupancy', 'hospital_id:1001', 89, 0.74, 'mock', CURRENT_TIMESTAMP, CURRENT_DATE + 7),
  (12002, 1001, 'medicine_demand', 'medicine_id:4001', 56, 0.81, 'mock', CURRENT_TIMESTAMP, CURRENT_DATE + 7),
  (12003, 1001, 'kit_demand', 'test_name:Dengue Rapid Test', 18, 0.79, 'mock', CURRENT_TIMESTAMP, CURRENT_DATE + 7)
ON CONFLICT (id) DO NOTHING;
