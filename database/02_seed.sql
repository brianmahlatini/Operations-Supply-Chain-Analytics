INSERT INTO regions (region_name, country, warehouse_name) VALUES
('Gauteng', 'South Africa', 'Johannesburg DC'),
('Western Cape', 'South Africa', 'Cape Town DC'),
('KwaZulu-Natal', 'South Africa', 'Durban DC'),
('Eastern Cape', 'South Africa', 'Gqeberha DC');

INSERT INTO suppliers (supplier_name, category, contracted_lead_time_days, risk_tier) VALUES
('Atlas Components', 'Electronics', 8, 'Low'),
('Harbor Packaging', 'Packaging', 5, 'Medium'),
('Northstar Textiles', 'Apparel', 12, 'High'),
('Prime Industrial', 'Industrial', 10, 'Medium'),
('FreshRoute Foods', 'Perishables', 4, 'Low');

INSERT INTO products (sku, product_name, category, supplier_id, unit_cost, reorder_point, target_stock) VALUES
('EL-1001', 'Smart Sensor Module', 'Electronics', 1, 185.00, 180, 520),
('EL-1002', 'Control Board', 'Electronics', 1, 265.00, 120, 360),
('PK-2201', 'Recycled Carton 10kg', 'Packaging', 2, 18.50, 500, 1600),
('PK-2202', 'Tamper Seal Roll', 'Packaging', 2, 9.80, 650, 1900),
('AP-3101', 'Workwear Jacket', 'Apparel', 3, 145.00, 160, 450),
('AP-3102', 'Safety Glove Pair', 'Apparel', 3, 34.00, 420, 1300),
('IN-4401', 'Hydraulic Valve', 'Industrial', 4, 390.00, 90, 260),
('IN-4402', 'Bearing Kit', 'Industrial', 4, 118.00, 170, 520),
('FR-5501', 'Cold Chain Meal Kit', 'Perishables', 5, 62.00, 300, 900),
('FR-5502', 'Fresh Produce Crate', 'Perishables', 5, 41.00, 360, 1100);
