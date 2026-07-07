CREATE TABLE suppliers
(
  id SERIAL PRIMARY KEY,
  supplier_name VARCHAR(255),
  delivery_days INTEGER,
  reliability FLOAT,
  contact VARCHAR(255),
  active_orders INTEGER DEFAULT 0
);
CREATE INDEX ix_suppliers_supplier_name ON suppliers (supplier_name);