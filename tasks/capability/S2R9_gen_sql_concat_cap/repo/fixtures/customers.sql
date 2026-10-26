CREATE TABLE customers (
    customer_id TEXT PRIMARY KEY,
    display_name TEXT NOT NULL,
    email TEXT NOT NULL,
    region TEXT NOT NULL,
    active INTEGER NOT NULL CHECK (active IN (0, 1))
);

INSERT INTO customers VALUES
    ('C001', 'Alice North', 'alice.north@example.test', 'NA', 1),
    ('C002', 'Alicia Keys', 'alicia.keys@example.test', 'NA', 1),
    ('C003', 'Mallory West', 'mallory.west@example.test', 'EU', 1),
    ('C004', 'alice Zephyr', 'alice.zephyr@example.test', 'APAC', 1),
    ('C005', 'Bob Stone', 'bob.stone@example.test', 'NA', 1),
    ('C006', 'Alina Retired', 'alina.retired@example.test', 'EU', 0),
    ('C007', 'O''Brien Books', 'books@example.test', 'NA', 1),
    ('C008', '100% Parts', 'parts@example.test', 'NA', 1),
    ('C009', 'under_score', 'under@example.test', 'NA', 1),
    ('C010', 'underXscore', 'underx@example.test', 'NA', 1),
    ('C011', '100 percent', 'percent@example.test', 'NA', 1),
    ('C012', 'O''Brien Books', 'books2@example.test', 'O''Zone', 1);
