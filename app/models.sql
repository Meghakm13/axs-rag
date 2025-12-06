-- app/models.sql

-- Cleanup for development
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS customers;

-- =========================
-- Tables
-- =========================

CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    city VARCHAR(100),
    created_at DATE NOT NULL
);

CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    role VARCHAR(50),
    hired_at DATE NOT NULL
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price NUMERIC(12, 2) NOT NULL -- INR values
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL REFERENCES customers(id),
    employee_id INT NOT NULL REFERENCES employees(id),
    order_date DATE NOT NULL,
    total_amount NUMERIC(12, 2) NOT NULL
);

CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INT NOT NULL REFERENCES orders(id),
    product_id INT NOT NULL REFERENCES products(id),
    quantity INT NOT NULL,
    line_total NUMERIC(12, 2) NOT NULL
);

-- =========================
-- Sample data
-- =========================

-- Customers
INSERT INTO customers (name, city, created_at) VALUES
('Rajesh Kumar',       'Mumbai',      '2023-01-10'),
('Priya Sharma',       'Delhi',       '2023-02-15'),
('Amit Verma',         'Bengaluru',   '2023-03-05'),
('Neha Singh',         'Pune',        '2023-04-20'),
('Sanjay Patel',       'Ahmedabad',   '2023-05-12'),
('Ananya Iyer',        'Chennai',     '2023-06-18'),
('Farhan Khan',        'Hyderabad',   '2023-07-25'),
('Kritika Joshi',      'Jaipur',      '2023-08-02'),
('Vikram Deshmukh',    'Nagpur',      '2023-09-10'),
('Pooja Gupta',        'Kolkata',     '2023-10-01');

-- Employees 
INSERT INTO employees (name, role, hired_at) VALUES
('Sandeep Desai',     'Sales Executive',     '2022-01-15'),
('Kiran Patil',       'Relationship Manager','2021-06-10'),
('Anjali Rao',        'Support Executive',   '2022-09-01'),
('Manish Tiwari',     'Territory Manager',   '2020-11-20'),
('Sneha Kulkarni',    'Sales Executive',     '2023-01-05'),
('Ravi Shankar',      'Relationship Manager','2022-05-30'),
('Deepa Nair',        'Support Executive',   '2021-12-12'),
('Arjun Mehta',       'Sales Executive',     '2023-03-22');

-- Products
INSERT INTO products (name, category, price) VALUES
('UPI QR Standee',              'Payments',       299.00),
('POS Machine Basic',           'Payments',     18000.00),
('POS Machine Pro',             'Payments',     32000.00),
('Billing Software Starter',    'Software',      7999.00),
('Billing Software Premium',    'Software',     14999.00),
('Thermal Receipt Printer',     'Hardware',      6500.00),
('Barcode Scanner',             'Hardware',      4200.00),
('Cash Drawer',                 'Hardware',      3500.00),
('Android Handheld Device',     'Payments',     25000.00),
('Retail Analytics Add-on',     'Software',      4999.00);

-- Orders (spread across months/years, INR totals)
INSERT INTO orders (customer_id, employee_id, order_date, total_amount) VALUES
(1, 1, '2023-01-25',  18599.00), -- Rajesh, UPI + POS Basic
(2, 2, '2023-02-28',  39999.00), -- Priya, POS Pro + Printer
(3, 1, '2023-03-15',  22999.00), -- Amit, Billing Starter + QR
(4, 3, '2023-04-05',  28500.00), -- Neha, POS Basic + Scanner
(5, 4, '2023-05-20',  49999.00), -- Sanjay, POS Pro + Billing Premium
(6, 5, '2023-06-10',  31500.00), -- Ananya, Android Device + QR
(7, 6, '2023-07-18',  21499.00), -- Farhan, Billing Starter + Scanner
(8, 2, '2023-08-25',  45999.00), -- Kritika, POS Pro + Analytics
(9, 7, '2023-09-30',  27999.00), -- Vikram, Android Device + QR + Standee
(10,3, '2023-10-15',  18999.00), -- Pooja, Billing Starter + QR

-- Some 2024 orders for "last year"/"this year" type questions
(1, 8, '2024-01-08',  52999.00),
(3, 1, '2024-02-11',  35999.00),
(5, 2, '2024-03-19',  28999.00),
(7, 4, '2024-04-22',  61999.00),
(9, 5, '2024-05-05',  45999.00);

-- Order Items (make sure totals roughly match orders.total_amount)
-- Order 1 (id=1)
INSERT INTO order_items (order_id, product_id, quantity, line_total) VALUES
(1, 1, 1,   299.00),     -- UPI QR Standee
(1, 2, 1, 18000.00);     -- POS Machine Basic

-- Order 2 (id=2)
INSERT INTO order_items (order_id, product_id, quantity, line_total) VALUES
(2, 3, 1, 32000.00),     -- POS Machine Pro
(2, 6, 1,  6500.00),     -- Thermal Receipt Printer
(2, 1, 1,   499.00);     -- QR Standee slight mismatch for variety

-- Order 3 (id=3)
INSERT INTO order_items (order_id, product_id, quantity, line_total) VALUES
(3, 4, 1,  7999.00),     -- Billing Starter
(3, 1, 3,   897.00),     -- 3 x QR
(3, 7, 1,  4200.00);

-- Order 4 (id=4)
INSERT INTO order_items (order_id, product_id, quantity, line_total) VALUES
(4, 2, 1, 18000.00),
(4, 7, 1,  4200.00);

-- Order 5 (id=5)
INSERT INTO order_items (order_id, product_id, quantity, line_total) VALUES
(5, 3, 1, 32000.00),
(5, 5, 1, 14999.00);

-- Order 6 (id=6)
INSERT INTO order_items (order_id, product_id, quantity, line_total) VALUES
(6, 9, 1, 25000.00),
(6, 1, 5,  1495.00),
(6, 6, 1,  6500.00);

-- Order 7 (id=7)
INSERT INTO order_items (order_id, product_id, quantity, line_total) VALUES
(7, 4, 1,  7999.00),
(7, 7, 2,  8400.00),
(7, 1, 2,   598.00);

-- Order 8 (id=8)
INSERT INTO order_items (order_id, product_id, quantity, line_total) VALUES
(8, 3, 1, 32000.00),
(8,10,1,  4999.00),
(8, 1, 1,   299.00);

-- Order 9 (id=9)
INSERT INTO order_items (order_id, product_id, quantity, line_total) VALUES
(9, 9, 1, 25000.00),
(9, 1, 2,   598.00),
(9, 2, 1, 18000.00);

-- Order 10 (id=10)
INSERT INTO order_items (order_id, product_id, quantity, line_total) VALUES
(10,4, 1,  7999.00),
(10,1, 2,   598.00);

-- Orders 11–15 (2024)
INSERT INTO order_items (order_id, product_id, quantity, line_total) VALUES
(11,3, 1, 32000.00),
(11,6, 1,  6500.00),
(11,1, 2,   598.00),

(12,2, 1, 18000.00),
(12,4, 1,  7999.00),
(12,7, 1,  4200.00),

(13,5, 1, 14999.00),
(13,1, 3,   897.00),
(13,8, 1,  3500.00),

(14,3, 1, 32000.00),
(14,9, 1, 25000.00),

(15,2, 1, 18000.00),
(15,10,1,  4999.00),
(15,1, 2,   598.00);
