-- 0001_init.sql — initial schema for the target database.
CREATE TABLE IF NOT EXISTS customers   (id INTEGER PRIMARY KEY, name TEXT, email TEXT, created_at TEXT);
CREATE TABLE IF NOT EXISTS orders       (id INTEGER PRIMARY KEY, customer_id INTEGER, total_cents INTEGER, status TEXT, created_at TEXT);
CREATE TABLE IF NOT EXISTS order_items  (id INTEGER PRIMARY KEY, order_id INTEGER, sku TEXT, qty INTEGER, price_cents INTEGER);
CREATE TABLE IF NOT EXISTS payments     (id INTEGER PRIMARY KEY, order_id INTEGER, amount_cents INTEGER, method TEXT, created_at TEXT);
CREATE TABLE IF NOT EXISTS addresses    (id INTEGER PRIMARY KEY, customer_id INTEGER, line1 TEXT, city TEXT, country TEXT);
